from sqlalchemy.orm import joinedload

from . import deal_inside_bp
from flask import (
    jsonify,
    request,
    render_template,
)
from logger import logging
from .sql_queries import (
    get_users_with_roles,
    update_deal_created_by,
    delete_seller_by_calc_id,
    delete_calculator_section,
    update_client_in_db,
)
from ..config import suggestions_token
from ..deal.models import Deal
from .. import socketio
from ..leasing_calculator.models import Seller


@deal_inside_bp.route("/<deal_id>", methods=["GET"])
def enter_into_deal(deal_id: int):
    # Находим сделку по deal_id, загружаем связанного клиента
    deal: Deal = Deal.query.options(
        joinedload(Deal.leas_calculators), joinedload(Deal.client)
    ).get(deal_id)

    # Проверяем, что сделка найдена
    if not deal:
        return "Сделка не найдена", 404

    # Получаем group_id сделки
    group_id = deal.group_id

    if group_id:
        logging.info(f"Group ID: {group_id}")
        # Получаем все связанные сделки по group_id, включая текущую сделку, загружаем клиентов
        related_deals = (
            Deal.query.options(
                joinedload(Deal.leas_calculators), joinedload(Deal.client)
            )
            .filter_by(group_id=group_id)
            .all()
        )
    else:
        logging.info("Group ID: None")
        # Если group_id пуст, возвращаем только текущую сделку
        related_deals = [deal]

    # Собираем информацию о связанных договорах и их лизинговых калькуляторах
    deals_info = []
    for related_deal in related_deals:
        # Получаем данные клиента
        client = related_deal.client

        if related_deal.leas_calculators:
            for leas_calc in related_deal.leas_calculators:
                deal_info = {
                    "leas_calc": leas_calc,
                    "dl_number": related_deal.dl_number,
                    "created_by": related_deal.created_by,
                    "created_at": related_deal.created_at,
                    "client": client,  # Добавляем информацию о клиенте
                }
                deals_info.append(deal_info)
        else:
            # Если у договора нет лизинговых калькуляторов, добавляем информацию о договоре без leas_calc
            deal_info = {
                "leas_calc": None,
                "dl_number": related_deal.dl_number,
                "created_by": related_deal.created_by,
                "created_at": related_deal.created_at,
                "client": client,  # Добавляем информацию о клиенте
            }
            deals_info.append(deal_info)

    logging.info(f"Deals info: {deals_info}")
    return render_template(
        "deal.html",
        deal=deal,
        deals_info=deals_info,  # Передаем список всех связанных договоров с их лизинговыми калькуляторами
        deal_id=deal_id,
        suggestions_token=suggestions_token,
    )


@deal_inside_bp.route("/get-managers-and-admins", methods=["GET"])
def get_managers_and_admins():
    current_user_id = request.args.get(
        "current_user_id"
    )  # Получаем текущего ответственного пользователя
    users = get_users_with_roles(["manager", "admin", "tester"], current_user_id)
    return jsonify(users)


@deal_inside_bp.route("/update-created-by/<int:deal_id>", methods=["POST"])
def update_created_by(deal_id):
    try:
        new_created_by = request.json.get("created_by")

        if not new_created_by:
            logging.error(
                f"Invalid input: 'created_by' not provided for deal_id {deal_id}"
            )
            return jsonify({"error": "Invalid input"}), 400

        deal, error = update_deal_created_by(deal_id, new_created_by)
        if error:
            if error == "Deal not found":
                logging.error(f"Deal not found: deal_id {deal_id}")
                return jsonify({"error": "Deal not found"}), 404
            else:
                logging.error(f"Error updating deal_id {deal_id}: {error}")
                return jsonify({"error": "Failed to update deal"}), 500

        logging.info(
            f"Deal updated successfully: deal_id {deal_id} updated to created_by {new_created_by}"
        )
        # Отправка уведомления всем пользователям в комнате
        socketio.emit(
            "update_created_by",
            {
                "message": f"Ответственный успешно обновлен на {new_created_by}",
                "new_created_by": new_created_by,  # Передаем новое значение
            },
            to=str(deal_id),
        )
        socketio.emit(
            "update_created_by_all",
            {
                "new_created_by": new_created_by,  # Передаем новое значение
                "deal_id": deal_id,
            },
        )
        return jsonify({"message": "Deal updated successfully"}), 200

    except Exception as e:
        logging.exception(
            f"Unexpected error occurred while updating deal_id {deal_id}: {str(e)}"
        )
        return jsonify({"error": "An unexpected error occurred"}), 500


@deal_inside_bp.route("/check-seller-inn", methods=["POST"])
def check_inn():
    inn = request.json.get("inn")

    if not inn:
        return jsonify({"error": "ИНН не предоставлен"}), 400

    # Поиск в базе данных
    seller = Seller.query.filter_by(inn=inn).first()

    if seller:
        return (
            jsonify(
                {
                    "name": seller.name,
                    "inn": seller.inn,
                    "address": seller.address,
                    "phone": seller.phone,
                    "email": seller.email,
                    "signer": seller.signer,
                }
            ),
            200,
        )
    else:
        return jsonify({"message": "Продавец не найден в базе"}), 404


@deal_inside_bp.route("/delete-seller", methods=["POST"])
def delete_seller():
    try:
        data = request.get_json()
        calc_id = data.get("calc_id")

        # Вызываем сервисную функцию для удаления seller_id
        success, message = delete_seller_by_calc_id(calc_id)

        if not success:
            return jsonify({"success": False, "message": message}), 404

        return jsonify({"success": True, "message": message}), 200

    except Exception as e:
        logging.exception(f"Ошибка при удалении продавца: {str(e)}")
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Ошибка при удалении поставщика",
                    "error": str(e),
                }
            ),
            500,
        )


@deal_inside_bp.route("/delete-section", methods=["POST"])
def delete_section():
    try:
        # Получаем данные из запроса
        data = request.get_json()
        calc_id = data.get("calc_id")
        dl_number = data.get("dl_number")

        # Вызов функции для удаления секции
        success, message = delete_calculator_section(calc_id, dl_number)

        if success:
            return jsonify({"success": True, "message": message}), 200
        else:
            return jsonify({"success": False, "message": message}), 404

    except Exception as e:
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Ошибка при удалении секции",
                    "error": str(e),
                }
            ),
            500,
        )


@deal_inside_bp.route("/update-client", methods=["POST"])
def update_client_info():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "Нет данных в запросе"}), 400

    deal_id = data.get("deal_id")
    if not deal_id:
        return jsonify({"success": False, "message": "Не указан deal_id"}), 400

    # Получаем обновленную информацию о клиенте
    new_address = data.get("address")
    new_phone = data.get("phone")
    new_email = data.get("email")
    new_signer = data.get("signer")

    # Вызываем функцию обновления клиента в базе данных
    response_data, status_code = update_client_in_db(
        deal_id, new_address, new_phone, new_email, new_signer
    )

    return jsonify(response_data), status_code
