import datetime

from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from . import deal_bp
from .. import socketio, db

from .deals_db import write_deal_to_db
from .deals_validate import DealsValidate
from .work_with_folders import CompanyFolderAPI

from ..deal.models import Deal
from ..user.models import User
from ..config import suggestions_token

from flask import (
    request,
    jsonify,
    render_template,
    session,
    url_for,
)
from flask_login import current_user, login_required
from logger import logging


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
def create_deal() -> jsonify:
    api_folder = CompanyFolderAPI()
    deal = DealsValidate(request.get_json())
    company_name = deal.get_company_name
    name_without_special_symbols = deal.get_name_without_special_symbols
    company_inn = deal.get_company_inn

    try:
        # Проверка доступности API
        if not api_folder.is_available():
            raise Exception("CompanyFolderAPI недоступен")

        # Запись сделки в базу данных
        deal_data = write_deal_to_db(
            company_name,
            name_without_special_symbols,
            company_inn,
            current_user.fullname,
            datetime.datetime.now(),
        )
        deal_id = str(deal_data["id"])
        dl_number = deal_data["dl_number_windows"]

        # Создание папки через API
        api_folder.create_folder(name_without_special_symbols, deal_id, dl_number)

        # Логирование и уведомление
        logging.info(
            f"{current_user} создал новую сделку. Название сделки: {company_name}. "
            f"ID сделки: {deal_id}. Дата создания: {deal_data['created_at']}."
        )
        socketio.emit("new_deal", deal_data)  # Send to all connected clients

        # Определяем, куда отправлять уведомление
        session_username = session.get("username")
        logging.info(f"session: {session}")
        logging.info(f"session_username (create deal): {session_username}")
        if session_username:
            socketio.emit(
                "notification_new_deal",
                {"message": company_name},
                room=session_username,
            )
        else:
            logging.info(
                "Не удалось отправить уведомление: session_username не найден."
            )

        return jsonify(deal_data), 201

    except Exception as e:
        # Откат транзакции в случае ошибки
        db.session.rollback()
        logging.error(f"Ошибка при создании сделки: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@deal_bp.route("/crm/deal/delete_deal/<int:deal_id>", methods=["POST"])
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
            session_username = session.get("username")
            if session_username:
                socketio.emit(
                    "notification_delete_deal_well",
                    {"message": deal.title},
                    room=session_username,
                )
            else:
                logging.info(
                    "Не удалось отправить уведомление: session_username не найден."
                )
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
def deal_to_archive(deal_id) -> jsonify:
    deal: Deal = Deal.query.get(deal_id)
    api_folder: CompanyFolderAPI = CompanyFolderAPI()
    if deal:
        try:
            # Начинаем транзакцию
            deal.status = "archived"
            deal.archived_at = datetime.datetime.now()
            old_dl_number = deal.dl_number_windows
            deal.dl_number = "б/н"
            deal.dl_number_windows = "б-н"
            db.session.commit()
            api_folder.active_or_archive_folder(deal_id, old_dl_number, "archive")
            socketio.emit("deal_to_archive", deal.to_json())
            session_username = session.get("username")
            if session_username:
                socketio.emit(
                    "notification_archive_deal_well",
                    {"message": deal.title},
                    room=session_username,
                )
            else:
                logging.info(
                    "Не удалось отправить уведомление: session_username не найден."
                )
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
                        "message": "Failed to archive deal from database",
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
            deal.dl_number, deal.dl_number_windows = Deal.generate_dl_number()
            db.session.commit()
            api_folder.active_or_archive_folder(
                deal_id, deal.dl_number_windows, "active"
            )
            socketio.emit("deal_to_active", deal.to_json())
            session_username = session.get("username")
            if session_username:
                socketio.emit(
                    "notification_active_deal_well",
                    {"message": deal.title},
                    room=session_username,
                )
            else:
                logging.info(
                    "Не удалось отправить уведомление: session_username не найден."
                )
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
@login_required
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
        user_name=current_user.fullname,
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


@deal_bp.route("/crm/deal/<deal_id>", methods=["GET"])
def enter_into_deal(deal_id: int) -> render_template:
    deal: Deal = Deal.query.get(deal_id)
    return render_template("deal.html", deal=deal)
