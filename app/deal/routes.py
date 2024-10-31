import datetime
from collections import defaultdict

from flask import (
    jsonify,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from logger import logging

from .. import db, socketio
from ..config import suggestions_token
from ..deal.models import Deal
from ..leasing_calculator.models import LeasCalculator
from ..user.auth_utils import _tester_required, validate_active_session
from ..user.models import User
from . import deal_bp
from .deals_db import get_or_create_client, write_deal_path_to_db, write_deal_to_db
from .deals_validate import DealsValidate
from .sql_queries import merge_deals_in_db
from .work_with_folders import CompanyFolderAPI


def send_notification(socket_path: str, error_message: str) -> jsonify:
    logging.info(f"Session now: {session}")
    session_username = session.get("username")
    logging.info(f"session_username: {session_username}")
    if session_username:
        socketio.emit(
            socket_path,
            {"message": error_message},
            room=session_username,
        )
    else:
        logging.info("Не удалось отправить уведомление: session_username не найден.")
    return jsonify({"result": "error", "message": error_message}), 500


@deal_bp.route("/crm/deal/create_deal", methods=["POST"])
@validate_active_session
def create_deal() -> jsonify:
    api_folder = CompanyFolderAPI()
    deal_data = request.get_json()
    deal = DealsValidate(deal_data)
    company_name = deal.get_company_name
    name_without_special_symbols = deal.get_name_without_special_symbols
    company_inn = deal.get_company_inn

    try:
        # Проверка доступности API
        if not api_folder.is_available():
            raise Exception("CompanyFolderAPI недоступен")

        # Обработка клиента
        client_id = get_or_create_client(deal)

        # Запись сделки в базу данных
        deal_record = write_deal_to_db(
            title=company_name,
            name_without_special_symbols=name_without_special_symbols,
            company_inn=company_inn,
            created_by=current_user.abbreviation_name,
            created_at=datetime.datetime.now(),
            client_id=client_id,
        )
        deal_id = str(deal_record["id"])
        dl_number = deal_record["dl_number_windows"]

        # Создание папки через API
        created_folder = api_folder.create_folder(
            name_without_special_symbols, deal_id, dl_number
        )  # Путь к папке со сделкой

        write_deal_path_to_db(
            created_folder, deal_id
        )  # Запись пути к папке (к сделке) в БД

        # Логирование и уведомление
        logging.info(
            f"{current_user.abbreviation_name} создал новую сделку. Название сделки: {company_name}. "
            f"ID сделки: {deal_id}. Дата создания: {deal_record['created_at']}."
        )
        socketio.emit("new_deal", deal_record)  # Send to all connected clients

        return jsonify(deal_record), 201

    except Exception as e:
        # Откат транзакции в случае ошибки
        db.session.rollback()
        logging.error(f"Ошибка при создании сделки: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@deal_bp.route("/crm/deal/delete_deal/<int:deal_id>", methods=["POST"])
@validate_active_session
def delete_deal(deal_id) -> jsonify:
    deal: Deal = Deal.query.get(deal_id)
    api_folder: CompanyFolderAPI = CompanyFolderAPI()
    if deal:
        try:
            # Начинаем транзакцию
            db.session.delete(deal)
            api_folder.delete_folder(deal_id)
            db.session.commit()

            # Уведомление через socketio
            socketio.emit("delete_deal", {"id": deal_id})

            return jsonify({"result": "success"}), 200

        except PermissionError as e:
            db.session.rollback()  # Откат транзакции в случае ошибки
            logging.error(f"Permission error while deleting deal {deal_id}: {e}")
            error_message: str = str(e).replace("[Errno 13] Permission denied: ", "")
            return send_notification("notification_delete_deal", error_message)

        except SQLAlchemyError as e:
            db.session.rollback()  # Откат транзакции в случае ошибки
            logging.error(f"Database error while deleting deal {deal_id}: {e}")
            return (
                jsonify(
                    {
                        "result": "error",
                        "message": "Failed to delete deal from database",
                    }
                ),
                500,
            )

        except Exception as e:
            db.session.rollback()  # Откат транзакции в случае ошибки
            logging.error(f"Error while deleting deal {deal_id} or company folder: {e}")
            return (
                jsonify(
                    {"result": "error", "message": "Failed to delete company folder"}
                ),
                500,
            )
    else:
        return jsonify({"result": "error", "message": "Deal not found"}), 404


@deal_bp.route("/crm/deal/deal_to_archive/<int:deal_id>", methods=["POST"])
@validate_active_session
def deal_to_archive(deal_id) -> jsonify:
    deal: Deal = Deal.query.get(deal_id)
    api_folder: CompanyFolderAPI = CompanyFolderAPI()
    if deal:
        try:
            # Получаем group_id основной сделки
            group_id = deal.group_id

            if group_id:
                # Находим все сделки с таким же group_id
                related_deals = Deal.query.filter_by(group_id=group_id).all()
            else:
                # Если group_id отсутствует, работаем только с текущей сделкой
                related_deals = [deal]

            # Начинаем транзакцию
            old_dl_numbers = (
                {}
            )  # Словарь для хранения исходных значений dl_number_windows

            for related_deal in related_deals:
                old_dl_number = (
                    related_deal.dl_number_windows
                )  # Сохраняем старое значение
                old_dl_numbers[related_deal.id] = (
                    old_dl_number  # Сохраняем в словарь с ключом id сделки
                )

                related_deal.status = "archived"
                related_deal.archived_at = datetime.datetime.now()
                related_deal.dl_number = "б/н"
                related_deal.dl_number_windows = "б-н"

            db.session.commit()

            # Обновляем пути к папкам для каждой сделки
            for related_deal in related_deals:
                old_dl_number = old_dl_numbers.get(
                    related_deal.id
                )  # Получаем старое значение из словаря

                path_to_folder = api_folder.active_or_archive_folder(
                    related_deal.id, old_dl_number, "archive"
                )
                logging.info("Обновляем путь к папке со сделкой (Архивная)")
                logging.info(f"New path: {path_to_folder}")
                logging.info(f"Deal ID: {related_deal.id}")
                write_deal_path_to_db(path_to_folder, related_deal.id)

                # Отправляем уведомление по SocketIO
                socketio.emit("deal_to_archive", related_deal.to_json())

            return jsonify({"result": "success"}), 200
        except PermissionError as e:
            db.session.rollback()  # Откат транзакции в случае ошибки
            logging.error(f"Permission error while archiving deal {deal_id}: {e}")
            error_message: str = str(e).replace("[Errno 13] Permission denied: ", "")
            return send_notification("notification_to_archive_deal", error_message)
        except SQLAlchemyError as e:
            db.session.rollback()  # Откат транзакции в случае ошибки
            logging.error(f"Database error while archiving deal {deal_id}: {e}")
            return (
                jsonify(
                    {
                        "result": "error",
                        "message": "Failed to archive deal in database",
                    }
                ),
                500,
            )
        except Exception as e:
            db.session.rollback()  # Откат транзакции в случае ошибки
            logging.error(
                f"Error while archiving deal {deal_id} or company folder: {e}"
            )
            return (
                jsonify(
                    {"result": "error", "message": "Failed to archive company folder"}
                ),
                500,
            )
    else:
        return jsonify({"result": "error", "message": "Deal not found"}), 404


@deal_bp.route("/crm/deal/deal_to_active/<int:deal_id>", methods=["POST"])
@validate_active_session
def deal_to_active(deal_id) -> jsonify:
    """Изменить статус сделки на активную"""

    deal: Deal = Deal.query.get(deal_id)
    api_folder: CompanyFolderAPI = CompanyFolderAPI()
    if deal:
        try:
            # Начинаем транзакцию
            deal.status = "active"
            deal.archived_at = None
            deal.created_at = datetime.datetime.now()
            deal.sequence_number, deal.year, deal.dl_number, deal.dl_number_windows = (
                Deal.generate_dl_number()
            )
            db.session.commit()
            path_to_folder = api_folder.active_or_archive_folder(
                deal_id, deal.dl_number_windows, "active"
            )
            logging.info("Обновляем путь к папке со сделкой (Активная)")
            logging.info(f"New path: {path_to_folder}")
            logging.info(f"Deal ID: {deal_id}")
            write_deal_path_to_db(path_to_folder, deal_id)

            socketio.emit("deal_to_active", deal.to_json())
            return jsonify({"result": "success"}), 200
        except PermissionError as e:
            db.session.rollback()  # Откат транзакции в случае ошибки
            logging.error(f"Permission error while return active deal {deal_id}: {e}")
            error_message: str = str(e).replace("[Errno 13] Permission denied: ", "")
            return send_notification("notification_to_active_deal", error_message)
        except SQLAlchemyError as e:
            db.session.rollback()  # Откат транзакции в случае ошибки
            logging.error(f"Database error while return active deal {deal_id}: {e}")
            return (
                jsonify(
                    {
                        "result": "error",
                        "message": "Failed to return active deal from database",
                    }
                ),
                500,
            )
        except Exception as e:
            db.session.rollback()  # Откат транзакции в случае ошибки
            logging.error(
                f"Error while return active deal {deal_id} or company folder: {e}"
            )
            return (
                jsonify(
                    {
                        "result": "error",
                        "message": "Failed to return active company folder",
                    }
                ),
                500,
            )
    return jsonify({"result": "error", "message": "Deal not found"}), 404


@deal_bp.route("/crm", methods=["GET"])
@_tester_required
@validate_active_session
def index_crm() -> render_template:
    session["username"] = current_user.login  # Устанавливаем username в сессию
    logging.info(f"Socket connected: {session}")
    logging.info(f"FON: {current_user.fon_url}")
    deals: list[Deal] = Deal.query.all()
    users: list[User] = User.query.all()

    # установка фона для пользователя
    user_fon_filename = current_user.fon_url
    user_fon_url = url_for("crm.static", filename=user_fon_filename)
    return render_template(
        "crm.html",
        deals=deals,
        users=users,
        user_name=current_user.abbreviation_name,
        user_email=current_user.email,
        user_role=current_user.role,
        user_login=current_user.login,
        user_url=current_user.url_photo,
        user_work_number=current_user.worknumber,
        user_mobile_number=current_user.mobilenumber,
        user_fon=user_fon_url,
        suggestions_token=suggestions_token,
    )


@deal_bp.route("/crm/deals/active", methods=["GET"])
def get_deals_active() -> jsonify:
    user_fullname = request.args.get(
        "user_fullname"
    )  # Получаем параметр из строки запроса

    # Получаем все активные сделки
    active_deals_query = Deal.query.filter_by(status="active").order_by(
        desc(Deal.created_at)
    )

    if user_fullname:
        active_deals_query = active_deals_query.filter_by(created_by=user_fullname)

    active_deals: list[Deal] = active_deals_query.all()
    active_deals_count: int = len(active_deals)
    archived_deals_count: int = Deal.query.filter_by(status="archived").count()

    # Группируем сделки по group_id
    grouped_deals = defaultdict(list)  # Для хранения сгруппированных сделок
    for deal in active_deals:
        group_key = (
            deal.group_id if deal.group_id else deal.id
        )  # Если нет group_id, используем id как ключ
        grouped_deals[group_key].append(deal)

    # Формируем ответ с объединенными сделками
    deals_response = []
    for _group, deals in grouped_deals.items():
        # Соединяем номера ДЛ через запятую
        dl_numbers = ", ".join([deal.dl_number for deal in deals])
        # Берем информацию из первой сделки в группе для остальных полей
        first_deal = deals[0]
        deals_response.append(
            {
                "id": first_deal.id,  # Используем id первой сделки для идентификатора строки
                "dl_number": dl_numbers,
                "product": first_deal.product,
                "title": first_deal.title,
                "company_inn": first_deal.company_inn,
                "created_by": first_deal.created_by,
                "created_at": first_deal.created_at.strftime("%Y-%m-%d %H:%M:%S.%f"),
            }
        )

    return jsonify(
        {
            "deals": deals_response,
            "deals_active": active_deals_count,
            "deals_archived": archived_deals_count,
        }
    )


@deal_bp.route("/crm/deals/active-for-bind", methods=["GET"])
def get_deals_active_for_bind() -> jsonify:
    user_fullname = request.args.get(
        "user_fullname"
    )  # Получаем параметр из строки запроса
    active_deals: list[Deal] = (
        Deal.query.filter_by(status="active").order_by(desc(Deal.created_at)).all()
    )
    active_deals_count: int = len(active_deals)
    archived_deals_count: int = Deal.query.filter_by(status="archived").count()
    if user_fullname:
        active_deals: list[Deal] = (
            Deal.query.filter_by(status="active", created_by=user_fullname)
            .order_by(desc(Deal.created_at))
            .all()
        )

    return jsonify(
        {
            "deals": [
                {
                    "id": deal.id,
                    "dl_number": deal.dl_number,
                    "product": deal.product,
                    "title": deal.title,
                    "company_inn": deal.company_inn,
                    "created_by": deal.created_by,
                    "created_at": deal.created_at.strftime("%Y-%m-%d %H:%M:%S.%f"),
                    "leas_calc": (
                        "(КП подвязано)"
                        if LeasCalculator.query.filter_by(deal_id=deal.id).first()
                        else ""
                    ),
                }
                for deal in active_deals
            ],
            "deals_active": active_deals_count,
            "deals_archived": archived_deals_count,
        }
    )


@deal_bp.route("/crm/deals/archived", methods=["GET"])
def get_deals_archived() -> jsonify:
    archived_deals: list[Deal] = (
        Deal.query.filter_by(status="archived").order_by(desc(Deal.archived_at)).all()
    )
    active_deals_count: int = Deal.query.filter_by(status="active").count()
    archived_deals_count: int = len(archived_deals)
    return jsonify(
        {
            "deals": [
                {
                    "id": deal.id,
                    "dl_number": deal.dl_number,
                    "title": deal.title,
                    "product": deal.product,
                    "company_inn": deal.company_inn,
                    "created_by": deal.created_by,
                    "created_at": deal.created_at.strftime("%Y-%m-%d %H:%M:%S.%f"),
                    "archived_at": deal.archived_at.strftime("%Y-%m-%d %H:%M:%S.%f"),
                }
                for deal in archived_deals
            ],
            "deals_active": active_deals_count,
            "deals_archived": archived_deals_count,
        }
    )


@deal_bp.route("/crm/deals/merge-deals", methods=["POST"])
def merge_deals():
    try:
        data = request.get_json()
        deal_ids = data.get("deals")

        if len(deal_ids) < 2:
            return (
                jsonify(
                    {"success": False, "message": "Необходимо выбрать минимум 2 сделки"}
                ),
                400,
            )

        # Получаем сделки из базы данных по переданным ID
        selected_deals = Deal.query.filter(Deal.id.in_(deal_ids)).all()

        if not selected_deals:
            return jsonify({"success": False, "message": "Сделки не найдены"}), 404

        # Проверяем, что все сделки принадлежат одной компании и одному менеджеру
        first_company_inn = selected_deals[0].company_inn
        first_manager = selected_deals[0].created_by

        for deal in selected_deals:
            if (
                deal.company_inn != first_company_inn
                or deal.created_by != first_manager
            ):
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "Все сделки должны принадлежать одному лизингополучателю и одному менеджеру",
                        }
                    ),
                    400,
                )

        # Если проверки пройдены, выполняем объединение сделок
        group_id, error = merge_deals_in_db(deal_ids)

        if error:
            return jsonify({"error": error}), 404

        socketio.emit("update_deals_table")
        return jsonify({"success": True, "message": "Сделки успешно объединены"}), 200

    except Exception as e:
        logging.exception(f"Error while merging deals: {str(e)}")
        return (
            jsonify(
                {"success": False, "message": "Произошла ошибка при объединении сделок"}
            ),
            500,
        )


@deal_bp.route("/crm/deals/group/<int:deal_id>", methods=["GET"])
def get_deals_by_group(deal_id):
    deal = Deal.query.get(deal_id)
    if not deal:
        return jsonify({"error": "Сделка не найдена"}), 404

    if deal.group_id:
        # Если у сделки есть group_id, получаем все сделки с этим group_id
        grouped_deals = Deal.query.filter_by(group_id=deal.group_id).all()
        return (
            jsonify(
                {
                    "group_id": deal.group_id,
                    "deals": [
                        {
                            "id": d.id,
                            "dl_number": d.dl_number,
                            "company": d.title,  # Измените на правильное поле для компании
                            "manager": d.created_by,  # Измените на правильное поле для менеджера
                        }
                        for d in grouped_deals
                    ],
                }
            ),
            200,
        )
    else:
        # Если group_id нет, возвращаем только текущую сделку
        return (
            jsonify(
                {
                    "group_id": None,
                    "deals": [
                        {
                            "id": deal.id,
                            "dl_number": deal.dl_number,
                            "company": deal.title,  # Измените на правильное поле для компании
                            "manager": deal.created_by,  # Измените на правильное поле для менеджера
                        }
                    ],
                }
            ),
            200,
        )
