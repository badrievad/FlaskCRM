import json
from datetime import date
from pathlib import Path

from flask import (
    request,
    jsonify,
    render_template,
    url_for,
    current_app,
    send_file,
)
from flask_login import current_user, login_required
from sqlalchemy import desc
from sqlalchemy.orm import joinedload

from logger import logging
from . import leas_calc_bp
from .api_cb_rf import CentralBankExchangeRates, CentralBankKeyRate
from .api_for_leas_culc import upload_schedule
from .api_yandex_cloud import yandex_download_file_s3, yandex_delete_file_s3
from .other_utils import validate_item_price
from .pydantic_models import ValidateFields
from .sql_queries import create_or_update_seller_and_link_to_leas_calc
from .. import db, cache
from ..celery_utils import is_celery_alive
from ..config import FORM_OFFERS_PATH
from ..deal.deals_validate import DealsValidate
from ..deal.models import Deal
from ..leasing_calculator.celery_tasks import long_task
from ..leasing_calculator.models import (
    LeasCalculator,
    LeasingItem,
    Tranches,
    Insurances,
    CalculateResultSchedule,
)
from ..leasing_calculator.services import update_calculation_service


@leas_calc_bp.route("/crm/calculator", methods=["GET"])
@login_required
def get_leasing_calculator() -> render_template:
    # установка фона для пользователя
    user_fon_filename = current_user.fon_url
    user_fon_url = url_for("crm.static", filename=user_fon_filename)

    # список расчетов
    user_login = current_user.login
    user_fullname = current_user.fullname

    calc_list = (
        LeasCalculator.query.options(
            joinedload(LeasCalculator.deal)
        )  # Предварительная загрузка связи deal
        .filter_by(manager_login=user_login)
        .order_by(desc(LeasCalculator.id))
        .all()
    )

    return render_template(
        "leasing_calculator.html",
        user_fon=user_fon_url,
        calc_list=calc_list,
        login=user_login,
        user_fullname=user_fullname,
    )


# Эндпоинт для запуска фоновой задачи
@leas_calc_bp.route("/crm/calculator/start-task", methods=["POST"])
def start_task() -> jsonify:
    data: dict = request.get_json()

    curr_user_path = FORM_OFFERS_PATH / current_user.login
    path_unvalid_data = curr_user_path / "unvalid_data.json"
    path_valid_data = curr_user_path / "valid_data.json"

    # Создание директории, если она не существует
    curr_user_path.mkdir(parents=True, exist_ok=True)

    with open(path_unvalid_data, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    validate_data: dict = ValidateFields(**data).model_dump()

    with open(path_valid_data, "w", encoding="utf-8") as f:
        json.dump(validate_data, f, ensure_ascii=False, indent=4)

    try:
        # Проверка состояния Celery
        if not is_celery_alive(current_app.extensions["celery"]):
            logging.info("Сервер Celery недоступен")
            return jsonify({"error": "Сервер временно недоступен"}), 503

        user_info: dict = {
            "user_login": current_user.login,
            "user_name": current_user.fullname,
            "user_email": current_user.email,
            "user_phone": current_user.mobilenumber,
        }
        logging.info(user_info)
        task = long_task.delay({**user_info, **validate_data})
        return jsonify({"task_id": task.id}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@leas_calc_bp.route("/crm/calculator/status/<task_id>", methods=["GET"])
def get_status(task_id) -> jsonify:
    try:
        task = long_task.AsyncResult(task_id)
        if task.state == "PENDING":
            response = {"state": task.state, "status": "Pending..."}
        elif task.state != "FAILURE":
            response = {"state": task.state, "status": task.info}
            if task.state == "SUCCESS" and task.result:
                response["result"] = {
                    "id": task.result.get("id"),
                    "title": task.result.get("title"),
                    "date_ru": task.result.get("date_ru"),
                    "manager_login": task.result.get("manager_login"),
                    "item_type": task.result.get("item_type"),
                    "item_name": task.result.get("item_name"),
                    "item_price": task.result.get("item_price"),
                    "item_price_str": task.result.get("item_price_str"),
                }
        else:
            response = {"state": task.state, "status": str(task.info)}
        current_app.logger.info(f"Task {task_id} status: {response}")
        return jsonify(response)
    except Exception as e:
        current_app.logger.error(f"Error fetching status for task {task_id}: {e}")
        return jsonify({"error": str(e)}), 500


@leas_calc_bp.route("/crm/calculator/delete/<int:calc_id>", methods=["POST"])
def delete_calculation(calc_id) -> jsonify:
    try:
        calc = LeasCalculator.query.filter_by(id=calc_id).first()
        if calc is None:
            return jsonify({"success": False, "message": "Calculation not found"}), 404

        # Найти связанный tranche, если он существует
        tranche = calc.tranche  # Получить связанную запись из Tranches
        insurance = calc.insurance  # Получить связанную запись из Insurances

        if tranche:
            db.session.delete(tranche)  # Удалить запись из Tranches

        if insurance:
            db.session.delete(insurance)  # Удалить запись из Insurances

        # Удалить файл из S3
        yandex_delete_file_s3(calc.title)

        db.session.delete(calc)  # Удалить запись из LeasCalculator
        db.session.commit()  # Подтвердить транзакцию

        return jsonify(
            {
                "success": True,
                "message": "Calculation and related tranche deleted successfully",
            }
        )

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "success": False,
                    "message": "An error occurred while deleting the calculation",
                    "error": str(e),
                }
            ),
            500,
        )


@leas_calc_bp.route("/crm/calculator/download/<int:calc_id>", methods=["GET"])
def download_calculation(calc_id):
    logging.info(f"Запрос на скачивание КП (id_{calc_id})")
    try:
        calc: LeasCalculator = LeasCalculator.query.filter_by(id=calc_id).first()
        if calc is None:
            return jsonify({"success": False, "message": "Calculation not found"}), 404

        file_name = f"Коммерческое предложение (id_{calc_id}).pdf"
        commercial_offer = yandex_download_file_s3(file_name)

        return send_file(commercial_offer, as_attachment=True)

    except Exception as e:
        logging.info(f"Ошибка при скачивании КП: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "message": "An error occurred while downloading the commercial offer",
                    "error": str(e),
                }
            ),
            500,
        )


@leas_calc_bp.route("/crm/calculator/autocomplete", methods=["GET"])
def autocomplete() -> jsonify:
    query = request.args.get("query", "")
    suggestions = (
        LeasingItem.query.filter(LeasingItem.name.ilike(f"%{query}%")).limit(10).all()
    )
    results = [item.name for item in suggestions]
    return jsonify(results)


@leas_calc_bp.route("/crm/calculator/update/<int:calc_id>", methods=["POST"])
def update_calculation(calc_id):
    try:
        if not request.is_json:
            logging.error("Request data is not in JSON format")
            return (
                jsonify(
                    {"success": False, "message": "Request data must be in JSON format"}
                ),
                400,
            )

        data = request.get_json()
        logging.info(f"Request to update calculation (id_{calc_id}): {data}")

        result = update_calculation_service(calc_id, data)
        return jsonify(result), result["status_code"]

    except Exception as e:
        logging.error(f"Error updating calculation: {str(e)}")
        return (
            jsonify(
                {
                    "success": False,
                    "message": "An error occurred while updating the calculation",
                    "error": str(e),
                }
            ),
            500,
        )


@leas_calc_bp.route("/crm/calculator/get_exchange_rates", methods=["GET"])
@cache.cached(timeout=600)
def get_exchange_rates() -> jsonify:
    api = CentralBankExchangeRates()
    exchange_rates: dict = api.get_exchange_rates()
    return jsonify(exchange_rates)


@leas_calc_bp.route("/crm/calculator/get_key_rate", methods=["GET"])
@cache.cached(timeout=36000)
def get_key_rate() -> jsonify:
    api = CentralBankKeyRate()
    key_rate = api.get_key_rate()
    return jsonify(key_rate)


@leas_calc_bp.route(
    "/crm/calculator/copy-commercial-offer/<int:calc_id>", methods=["GET"]
)
def get_commercial_offer(calc_id: int) -> jsonify:
    try:
        calc: LeasCalculator = LeasCalculator.query.filter_by(id=calc_id).first()
        if calc is None:
            return jsonify({"success": False, "message": "Calculation not found"}), 404

        tranches: Tranches = Tranches.query.filter_by(id=calc.trance_id).first()
        insurances: Insurances = Insurances.query.filter_by(
            id=calc.insurance_id
        ).first()

        result = {
            "calc": calc.to_dict(),
            "tranches": tranches.to_dict(),
            "insurances": insurances.to_dict(),
        }
        return jsonify({"success": True, "data": result})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@leas_calc_bp.route("/crm/commercial-offer/<int:calc_id>", methods=["GET"])
def show_commercial_offer(calc_id) -> render_template:
    today = date.today().strftime("%d.%m.%Y")
    user_info = {
        "login": request.args.get("user_login"),
        "name": request.args.get("name"),
        "email": request.args.get("email"),
        "phone": request.args.get("phone"),
    }

    leas_calc = (
        LeasCalculator.query.options(joinedload(LeasCalculator.deal))
        .filter_by(id=calc_id)
        .first()
    )
    vat = validate_item_price(
        str(float(leas_calc.item_price) - float(leas_calc.item_price) / 1.2)
    )  # выделяем НДС 20%
    initial_payment_percent = validate_item_price(
        str(leas_calc.initial_payment_percent)
    )
    schedules = CalculateResultSchedule.query.filter_by(calc_id=leas_calc.id).all()
    logging.info(schedules)
    return render_template(
        "commercial-offer.html",
        today=today,
        user=current_user,
        leas_calc=leas_calc,
        vat=vat,
        initial_payment_percent=initial_payment_percent,
        user_info=user_info,
        schedules=schedules,
    )


@leas_calc_bp.route("/crm/calculator/overheads", methods=["GET"])
def get_overheads() -> jsonify:
    try:
        overheads_path = Path("app").resolve() / "static" / "jsons" / "overheads.json"
        logging.info(overheads_path)
        with open(overheads_path, "r") as f:
            overheads = json.load(f)
        return jsonify(overheads)
    except FileNotFoundError:
        logging.error("File not found")
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        logging.error("Error decoding JSON")
        return jsonify({"error": "Error decoding JSON"}), 500
    except Exception as e:
        logging.error(str(e))
        return jsonify({"error": str(e)}), 500


@leas_calc_bp.route("/crm/calculator/api/upload_schedule", methods=["POST"])
def upload_schedules():
    data = request.get_json()  # принимаем JSON с графиками
    upload_schedule(data)

    return jsonify({"message": "Schedules successfully uploaded"}), 201


@leas_calc_bp.route("/crm/calculator/update-seller", methods=["POST"])
def update_seller():
    data = request.get_json()
    data_validated = DealsValidate(data)

    # Получаем новое имя и ИНН из данных запроса
    new_name = data_validated.get_company_name or data.get("title")
    new_inn = data_validated.get_company_inn or data.get("inn")
    deal_id = data.get("deal_id")

    if not new_name or not new_inn or not deal_id:
        return (
            jsonify({"error": "Invalid input: name, INN, and deal_id are required"}),
            400,
        )

    # Создаем или обновляем продавца и привязываем его к LeasCalculator
    response_data, status_code = create_or_update_seller_and_link_to_leas_calc(
        new_name, new_inn, deal_id
    )

    return jsonify(response_data), status_code
