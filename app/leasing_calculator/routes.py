import json
from datetime import date, datetime
from pathlib import Path

from flask import (  # type: ignore
    Response,
    current_app,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_login import current_user, login_required  # type: ignore
from sqlalchemy import desc  # type: ignore
from sqlalchemy.orm import joinedload  # type: ignore

from log_conf import logger

from .. import cache, db
from ..celery_utils import is_celery_alive
from ..config import FORM_OFFERS_PATH
from ..deal.deals_validate import DealsValidate
from ..leasing_calculator.celery_tasks import long_task
from ..leasing_calculator.models import (
    CommercialOffer,
    Insurances,
    LeasCalculator,
    LeasingItem,
    Tranches,
)
from ..leasing_calculator.services import update_calculation_service
from ..user.auth_utils import validate_active_session
from . import leas_calc_bp
from .api_cb_rf import CentralBankExchangeRates, CentralBankKeyRate
from .api_for_leas_calc import post_request_upload_file_site
from .api_pdf_generate import PDFGeneratorClient
from .api_yandex_cloud import (
    yandex_delete_file_s3,
    yandex_download_file_s3,
    yandex_upload_file_s3,
)
from .other_utils import validate_item_price
from .pydantic_models import ValidateFields
from .sql_queries import (
    create_commercial_offer_in_db,
    create_new_leas_calc,
    create_or_update_seller_and_link_to_leas_calc,
    get_list_of_commercial_offers,
    get_list_of_leas_calculators,
    write_information_to_leas_calc,
)


@leas_calc_bp.route("/crm/calculator", methods=["GET"])
@login_required
@validate_active_session
def get_leasing_calculator() -> str:
    # установка фона для пользователя
    user_fon_filename = current_user.fon_url
    user_fon_url = url_for("crm.static", filename=user_fon_filename)

    # список расчетов пользователя
    user_login = current_user.login
    user_fullname = current_user.fullname

    # Получаем текущую дату
    today = datetime.today().date()

    # Фильтруем расчеты по дате, чтобы выводить только сегодняшние
    calc_list = (
        LeasCalculator.query.options(
            joinedload(LeasCalculator.deal)  # Предварительная загрузка связи deal
        )
        .filter_by(manager_login=user_login, status="completed")
        .filter(LeasCalculator.date == today)  # Фильтр по текущей дате
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


@leas_calc_bp.route("/crm/calculator/update-table", methods=["GET"])
@login_required
def update_table() -> str:
    # Получаем даты начала и конца периода из параметров запроса
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")

    # Преобразуем строки дат в объекты datetime
    if start_date_str:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    else:
        start_date = datetime(1900, 1, 1)  # Начальная дата по умолчанию

    if end_date_str:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    else:
        end_date = datetime.now()  # Текущая дата по умолчанию

    # список расчетов пользователя в выбранный период
    user_login = current_user.login

    calc_list = (
        LeasCalculator.query.options(
            joinedload(LeasCalculator.deal)  # Предварительная загрузка связи deal
        )
        .filter(LeasCalculator.manager_login == user_login)
        .filter(LeasCalculator.status == "completed")
        .filter(LeasCalculator.date.between(start_date, end_date))
        .order_by(desc(LeasCalculator.id))
        .all()
    )

    # Рендерим только таблицу (в виде HTML)
    return render_template(
        "partials/_leasing_calculator_table.html",  # Создадим отдельный шаблон для таблицы
        calc_list=calc_list,
    )


@leas_calc_bp.route("/crm/calculator/<int:calc_id>", methods=["GET"])
@login_required
def get_leasing_calculator_by_id(calc_id: int) -> str:
    logger.info(f"Запрос на отображение расчета (id_{calc_id})")
    calc_list = get_list_of_leas_calculators(current_user.login, calc_id)
    return render_template(
        "leasing_calculator_by_id.html",
        calc_list=calc_list[0],
        leas_calculator_id=calc_id,
    )


@leas_calc_bp.route(
    "/crm/calculator/<int:leas_calculator_id>/create-commercial-offer", methods=["POST"]
)
@login_required
@validate_active_session
def create_commercial_offer(leas_calculator_id):
    # Получаем данные из формы
    type_of_schedule = request.form.get("type_of_schedule")
    include_rate = request.form.get("include_rate")

    # Вызываем функцию, которая создаст коммерческое предложение в базе данных
    success, offer_id = create_commercial_offer_in_db(
        leas_calculator_id, type_of_schedule
    )

    # Проверяем результат выполнения функции
    if success:
        user_info = {
            "user_login": current_user.login,
            "user_name": current_user.fullname,
            "user_email": current_user.email,
            "user_phone": current_user.mobilenumber,
            "user_telegram": current_user.telegram,
            "include_rate": include_rate,
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
            logger.info(f"Создание коммерческого предложения: {new_title_pdf}")
            offer.leas_calculator.title = new_title_pdf
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error generating PDF: {e}")
            logger.info("PDF не создался. Сервис недоступен.")

        logger.info(
            f"Коммерческое предложение успешно создано для графика: {type_of_schedule}. id_{offer_id}"
        )
    else:
        logger.info("Произошла ошибка при создании коммерческого предложения")

    # Возвращаем пользователя на предыдущую страницу
    return redirect(url_for("leas_calc.get_leasing_calculator") + "#created-proposals")


# Эндпоинт для запуска фоновой задачи
@leas_calc_bp.route("/crm/calculator/start-task", methods=["POST"])
def start_task() -> tuple[Response, int]:
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
            logger.info("Сервер Celery недоступен")
            return jsonify({"error": "Сервер временно недоступен"}), 503

        user_info: dict = {
            "user_login": current_user.login,
            "user_name": current_user.fullname,
            "user_email": current_user.email,
            "user_phone": current_user.mobilenumber,
            "user_telegram": current_user.telegram,
        }
        logger.info(user_info)
        task = long_task.delay({**user_info, **validate_data})
        return jsonify({"task_id": task.id}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@leas_calc_bp.route("/crm/calculator/status/<task_id>", methods=["GET"])
def get_status(task_id) -> tuple[Response, int]:
    try:
        task = long_task.AsyncResult(task_id)

        # Инициализируем response
        response = {"state": task.state, "status": None, "result": None}

        if task.state == "PENDING":
            response["status"] = "Pending..."

        elif task.state != "FAILURE":
            response["status"] = task.info

            if task.state == "SUCCESS" and task.result:
                calc_id = task.result.get("calc_id")

                if calc_id is not None:
                    logger.info(
                        f"Task {task_id} completed successfully. Calc_id: {calc_id}"
                    )

                    # Обновляем статус в базе данных
                    calculator = LeasCalculator.query.get(calc_id)
                    if calculator:
                        calculator.status = "completed"
                        db.session.commit()

                        response["result"] = {
                            "id": task.result.get("id"),
                            "title": task.result.get("title"),
                            "date_ru": task.result.get("date_ru"),
                            "manager_login": task.result.get("manager_login"),
                            "item_type": task.result.get("item_type"),
                            "item_name": task.result.get("item_name"),
                            "item_price": task.result.get("item_price"),
                            "item_price_str": task.result.get("item_price_str"),
                            "status": calculator.status,
                        }
                    else:
                        logger.warning(f"Calculator with Calc_id {calc_id} not found.")
                else:
                    logger.warning(f"Task {task_id} completed but no calc_id found.")
        else:
            response["status"] = str(task.info)
            current_app.logger.error(f"Task {task_id} failed with error: {task.info}")

        current_app.logger.info(f"Task {task_id} status: {response}")
        return jsonify(response), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching status for task {task_id}: {e}")
        return jsonify({"error": str(e), "task_id": None}), 500


@leas_calc_bp.route("/crm/calculator/delete/<int:calc_id>", methods=["POST"])
def delete_calculation(calc_id) -> tuple[Response, int]:
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

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Calculation and related tranche deleted successfully",
                }
            ),
            200,
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
@validate_active_session
def download_offers(calc_id):
    logger.info(f"Запрос на скачивание КП (id_{calc_id})")
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
        logger.info(f"Ошибка при скачивании КП: {e}")
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
@validate_active_session
def download_calc(calc_id):
    logger.info(f"Запрос на скачивание расчета (id_{calc_id})")
    try:
        file_name = f"Лизинговый калькулятор version 1.9_{calc_id}.xlsm"
        leas_calculate = yandex_download_file_s3(file_name)

        return send_file(leas_calculate, as_attachment=True)

    except Exception as e:
        logger.info(f"Ошибка при скачивании КП: {e}")
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
def autocomplete() -> Response:
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
            logger.error("Request data is not in JSON format")
            return (
                jsonify(
                    {"success": False, "message": "Request data must be in JSON format"}
                ),
                400,
            )

        data = request.get_json()
        logger.info(f"Request to update calculation (id_{calc_id}): {data}")

        result = update_calculation_service(calc_id, data)
        return jsonify(result), result["status_code"]

    except Exception as e:
        logger.error(f"Error updating calculation: {str(e)}")
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
def get_exchange_rates() -> Response:
    api = CentralBankExchangeRates()
    exchange_rates: dict = api.get_exchange_rates()
    return jsonify(exchange_rates)


@leas_calc_bp.route("/crm/calculator/get_key_rate", methods=["GET"])
@cache.cached(timeout=36000)
def get_key_rate() -> Response:
    api = CentralBankKeyRate()
    key_rate = api.get_key_rate()
    return jsonify(key_rate)


@leas_calc_bp.route(
    "/crm/calculator/copy-commercial-offer/<int:calc_id>", methods=["GET"]
)
def get_commercial_offer(calc_id: int) -> tuple[Response, int]:
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
        return jsonify({"success": True, "data": result}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@leas_calc_bp.route("/crm/commercial-offer/<int:offer_id>", methods=["GET"])
def show_commercial_offer(offer_id) -> str:
    today = date.today().strftime("%d.%m.%Y")
    user_info = {
        "login": request.args.get("user_login"),
        "name": request.args.get("name"),
        "email": request.args.get("email"),
        "phone": request.args.get("phone"),
        "telegram": request.args.get("telegram"),
        "include_rate": request.args.get("include_rate"),
    }

    com_offers_list = get_list_of_commercial_offers(
        user_info["login"], offer_id=offer_id
    )
    logger.info(com_offers_list)
    item_price = com_offers_list[0]["leas_calculator"].item_price
    initial_payment_percent = com_offers_list[0][
        "leas_calculator"
    ].initial_payment_percent

    vat = validate_item_price(
        str(float(item_price) - float(item_price) / 1.2)
    )  # выделяем НДС 20%
    initial_payment_percent = validate_item_price(str(initial_payment_percent))
    initial_payment = com_offers_list[0]["leas_calculator"].initial_payment_str

    return render_template(
        "commercial-offer.html",
        today=today,
        user=current_user,
        com_offer=com_offers_list[0],
        vat=vat,
        initial_payment_percent=initial_payment_percent,
        initial_payment=initial_payment,
        user_info=user_info,
    )


@leas_calc_bp.route("/crm/calculator/overheads", methods=["GET"])
def get_overheads() -> tuple[Response, int]:
    try:
        overheads_path = Path("app").resolve() / "static" / "jsons" / "overheads.json"
        logger.info(overheads_path)
        with open(overheads_path, "r") as f:
            overheads = json.load(f)
        return jsonify(overheads), 200
    except FileNotFoundError:
        logger.error("File not found")
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        logger.error("Error decoding JSON")
        return jsonify({"error": "Error decoding JSON"}), 500
    except Exception as e:
        logger.error(str(e))
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


@leas_calc_bp.route("/crm/calculator/upload-file", methods=["POST"])
def upload_file():
    logger.info("Запрос на загрузку файла в Yandex Object Storage")
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "Файл не загружен"}), 400

    try:
        calc_id = create_new_leas_calc(current_user.login)
        file.filename = f"Лизинговый калькулятор version 1.9_{calc_id}.xlsm"

        filename = file.filename
        logger.info(f"Имя файла: {filename}")
        yandex_upload_file_s3(file, filename)

        if calc_id:
            logger.info(f"Новый ID расчета: {calc_id}")
            response_data: dict = post_request_upload_file_site(filename, calc_id)

            if response_data.get("error"):
                calc = LeasCalculator.query.filter_by(id=calc_id).first()
                if calc:
                    db.session.delete(calc)
                    db.session.commit()  # Коммитим удаление, чтобы изменения сохранились
                raise Exception("Не удалось создать расчет")

            write_information_to_leas_calc(response_data, calc_id, filename)

        else:
            raise Exception("Не удалось создать расчет")

        return (
            jsonify(
                {
                    "message": "Расчет успешно создан. Данные сохранены в БД.",
                    "file_name": filename,
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Ошибка при загрузке файла: {str(e)}")
        return jsonify({"error": f"Ошибка при загрузке файла: {str(e)}"}), 500
