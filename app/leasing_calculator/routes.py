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
    redirect,
)
from flask_login import current_user, login_required
from sqlalchemy import desc
from sqlalchemy.orm import joinedload

from logger import logging
from . import leas_calc_bp
from .api_cb_rf import CentralBankExchangeRates, CentralBankKeyRate
from .api_pdf_generate import PDFGeneratorClient
from .api_yandex_cloud import yandex_download_file_s3, yandex_delete_file_s3
from .other_utils import validate_item_price
from .pydantic_models import ValidateFields
from .sql_queries import (
    create_or_update_seller_and_link_to_leas_calc,
    create_commercial_offer_in_db,
    get_list_of_commercial_offers,
)
from .. import db, cache
from ..celery_utils import is_celery_alive
from ..config import FORM_OFFERS_PATH
from ..deal.deals_validate import DealsValidate
from ..deal.work_with_folders import CompanyFolderAPI
from ..leasing_calculator.celery_tasks import long_task
from ..leasing_calculator.models import (
    LeasCalculator,
    LeasingItem,
    Tranches,
    Insurances,
    ScheduleAnnuity,
    CommercialOffer,
    MainAnnuity,
    ScheduleDifferentiated,
    MainDifferentiated,
    ScheduleRegression,
    MainRegression,
)
from ..leasing_calculator.services import update_calculation_service


@leas_calc_bp.route("/crm/calculator", methods=["GET"])
@login_required
def get_leasing_calculator() -> render_template:
    # установка фона для пользователя
    user_fon_filename = current_user.fon_url
    user_fon_url = url_for("crm.static", filename=user_fon_filename)

    # список расчетов пользователя
    user_login = current_user.login
    user_fullname = current_user.fullname

    calc_list = (
        LeasCalculator.query.options(
            joinedload(LeasCalculator.deal)  # Предварительная загрузка связи deal
        )
        .filter_by(manager_login=user_login)
        .order_by(desc(LeasCalculator.id))
        .all()
    )

    # Получаем список коммерческих предложений и присоединяем связанные таблицы
    com_offers_list = get_list_of_commercial_offers(user_login)

    # Рендерим шаблон с переданными данными
    return render_template(
        "leasing_calculator.html",
        user_fon=user_fon_url,
        calc_list=calc_list,
        login=user_login,
        user_fullname=user_fullname,
        com_offers_list=com_offers_list,
    )


@leas_calc_bp.route("/crm/calculator/<int:calc_id>", methods=["GET"])
@login_required
def get_leasing_calculator_by_id(calc_id: int) -> render_template:
    logging.info(f"Запрос на отображение расчета (id_{calc_id})")
    calc = LeasCalculator.query.get(calc_id)
    return render_template(
        "leasing_calculator_by_id.html", calc=calc, leas_calculator_id=calc_id
    )


@leas_calc_bp.route(
    "/crm/calculator/<int:leas_calculator_id>/create-commercial-offer", methods=["POST"]
)
@login_required
def create_commercial_offer(leas_calculator_id):
    # Получаем данные из формы
    type_of_schedule = request.form.get("type_of_schedule")

    # Вызываем функцию, которая создаст коммерческое предложение в базе данных
    success, offer_id = create_commercial_offer_in_db(
        leas_calculator_id, type_of_schedule
    )

    # Проверяем результат выполнения функции
    if success:
        folder_api = CompanyFolderAPI()
        user_info = {
            "user_login": current_user.login,
            "user_name": current_user.fullname,
            "user_email": current_user.email,
            "user_phone": current_user.mobilenumber,
        }
        pdf_api = PDFGeneratorClient(offer_id, user_info)

        offer = (
            CommercialOffer.query.options(
                joinedload(
                    CommercialOffer.leas_calculator
                )  # Предварительная загрузка связи leas_calc
            )
            .filter_by(leas_calculator_id=leas_calculator_id)
            .first()
        )

        try:
            pdf_api.generate_pdf()
            new_title_pdf = f"Коммерческое предложение (id_{offer_id}).pdf"
            logging.info(f"Создание коммерческого предложения: {new_title_pdf}")
            offer.leas_calculator.title = new_title_pdf
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error generating PDF: {e}")
            logging.info("PDF не создался. Сервис недоступен.")

        logging.info(
            f"Коммерческое предложение успешно создано для графика: {type_of_schedule}. id_{offer_id}"
        )
    else:
        logging.info("Произошла ошибка при создании коммерческого предложения")

    # Возвращаем пользователя на предыдущую страницу
    return redirect(url_for("leas_calc.get_leasing_calculator"))


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
        offer = (
            CommercialOffer.query.options(
                joinedload(
                    CommercialOffer.leas_calculator
                )  # Предварительная загрузка связи leas_calc
            )
            .filter_by(id=calc_id)
            .first()
        )

        if offer is None:
            return jsonify({"success": False, "message": "Calculation not found"}), 404

        # Удалить файл из S3
        yandex_delete_file_s3(offer.leas_calculator.title)

        db.session.delete(offer)  # Удалить запись из LeasCalculator
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
def download_offers(calc_id):
    logging.info(f"Запрос на скачивание КП (id_{calc_id})")
    try:
        offer = (
            CommercialOffer.query.options(
                joinedload(
                    CommercialOffer.leas_calculator
                )  # Предварительная загрузка связи leas_calc
            )
            .filter_by(id=calc_id)
            .first()
        )
        if offer is None:
            return jsonify({"success": False, "message": "Calculation not found"}), 404

        file_name = f"Коммерческое предложение (id_{offer.id}).pdf"
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


@leas_calc_bp.route("/crm/calculator/leas-calc-download/<int:calc_id>", methods=["GET"])
def download_calc(calc_id):
    logging.info(f"Запрос на скачивание расчета (id_{calc_id})")
    try:
        file_name = f"Лизинговый калькулятор version 1.8_{calc_id}.xlsm"
        leas_calculate = yandex_download_file_s3(file_name)

        return send_file(leas_calculate, as_attachment=True)

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


@leas_calc_bp.route("/crm/commercial-offer/<int:offer_id>", methods=["GET"])
def show_commercial_offer(offer_id) -> render_template:
    today = date.today().strftime("%d.%m.%Y")
    user_info = {
        "login": request.args.get("user_login"),
        "name": request.args.get("name"),
        "email": request.args.get("email"),
        "phone": request.args.get("phone"),
    }

    com_offers_list = get_list_of_commercial_offers(
        user_info["login"], offer_id=offer_id
    )
    logging.info(com_offers_list)
    item_price = com_offers_list[0]["leas_calculator"].item_price
    initial_payment_percent = com_offers_list[0][
        "leas_calculator"
    ].initial_payment_percent

    vat = validate_item_price(
        str(float(item_price) - float(item_price) / 1.2)
    )  # выделяем НДС 20%
    initial_payment_percent = validate_item_price(str(initial_payment_percent))

    return render_template(
        "commercial-offer.html",
        today=today,
        user=current_user,
        com_offer=com_offers_list[0],
        vat=vat,
        initial_payment_percent=initial_payment_percent,
        user_info=user_info,
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


@leas_calc_bp.route("/crm/calculator/update-seller", methods=["POST"])
def update_seller():
    data = request.get_json()
    data_validated = DealsValidate(data)

    # Получаем новое имя и ИНН из данных запроса
    new_name = data_validated.get_company_name or data.get("title")
    new_inn = data_validated.get_company_inn or data.get("inn")
    new_address = data.get("address")
    new_phone = data.get("phone")
    new_email = data.get("email")
    new_signer = data.get("signer")
    calc_id = data.get("calc_id")
    based_on = data.get("based_on")
    bank = json.loads(data.get("bank")) if data.get("bank") else None
    current = data.get("current")

    if not new_name or not new_inn or not calc_id:
        return (
            jsonify({"error": "Invalid input: name, INN, and deal_id are required"}),
            400,
        )

    # Создаем или обновляем продавца и привязываем его к LeasCalculator
    response_data, status_code = create_or_update_seller_and_link_to_leas_calc(
        new_name,
        new_inn,
        new_address,
        new_phone,
        new_email,
        new_signer,
        calc_id,
        based_on,
        bank,
        current,
    )

    return jsonify(response_data), status_code
