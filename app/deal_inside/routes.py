import json

from flask import (
    jsonify,
    render_template,
    request,
)
from sqlalchemy.orm import joinedload

from log_conf import logger

from .. import socketio
from ..config import suggestions_token
from ..deal.models import Client, Deal
from ..deal.risk_department.models import RiskDepartment
from ..leasing_calculator.models import LeasCalculator, Seller
from ..user.auth_utils import validate_active_session
from . import deal_inside_bp
from .sql_queries import (
    delete_calculator_section,
    delete_seller_by_calc_id,
    get_users_with_roles,
    update_client_in_db,
    update_deal_created_by,
)


@deal_inside_bp.route("/<deal_id>", methods=["GET"])
@validate_active_session
def enter_into_deal(deal_id: int):
    # Загрузка сделки, лизинговых калькуляторов, продавца, банка продавца, клиента и банка клиента
    deal: Deal = Deal.query.options(
        joinedload(Deal.leas_calculators)
        .joinedload(LeasCalculator.seller)
        .joinedload(Seller.bank),
        joinedload(Deal.client).joinedload(Client.bank),
    ).get(deal_id)

    # Проверяем, что сделка найдена
    if not deal:
        return "Сделка не найдена", 404

    # Получаем group_id сделки
    group_id = deal.group_id

    if group_id:
        logger.info(f"Group ID: {group_id}")
        # Получаем все связанные сделки по group_id
        related_deals = (
            Deal.query.options(
                joinedload(Deal.leas_calculators)
                .joinedload(LeasCalculator.seller)
                .joinedload(Seller.bank),
                joinedload(Deal.client).joinedload(Client.bank),
            )
            .filter_by(group_id=group_id)
            .all()
        )
    else:
        logger.info("Group ID: None")
        # Если group_id пуст, возвращаем только текущую сделку
        related_deals = [deal]

    # Собираем информацию о связанных договорах и их лизинговых калькуляторах
    deals_info = []
    for related_deal in related_deals:
        # Получаем данные клиента и его банка
        client = related_deal.client
        client_bank = client.bank if client else None

        if related_deal.leas_calculators:
            for leas_calc in related_deal.leas_calculators:
                # Получаем данные продавца и его банка
                seller = leas_calc.seller
                seller_bank = seller.bank if seller else None

                deal_info = {
                    "leas_calc": leas_calc,
                    "dl_number": related_deal.dl_number,
                    "created_by": related_deal.created_by,
                    "created_at": related_deal.created_at,
                    "client": client,  # Информация о клиенте
                    "client_bank": client_bank,  # Информация о банке клиента
                    "seller": seller,  # Информация о продавце
                    "seller_bank": seller_bank,  # Информация о банке продавца
                }
                deals_info.append(deal_info)
        else:
            # Если у сделки нет лизинговых калькуляторов
            deal_info = {
                "leas_calc": None,
                "dl_number": related_deal.dl_number,
                "created_by": related_deal.created_by,
                "created_at": related_deal.created_at,
                "client": client,
                "client_bank": client_bank,
                "seller": None,
                "seller_bank": None,
            }
            deals_info.append(deal_info)

    logger.info(f"Deals info: {deals_info}")

    # Получаем решение из базы данных
    risk_record = RiskDepartment.query.filter_by(deal_id=deal_id).first()
    decision = risk_record.decision if risk_record else None

    return render_template(
        "deal.html",
        deal=deal,
        deals_info=deals_info,
        deal_id=deal_id,
        suggestions_token=suggestions_token,
        decision=decision,
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
            logger.error(
                f"Invalid input: 'created_by' not provided for deal_id {deal_id}"
            )
            return jsonify({"error": "Invalid input"}), 400

        deal, error = update_deal_created_by(deal_id, new_created_by)
        if error:
            if error == "Deal not found":
                logger.error(f"Deal not found: deal_id {deal_id}")
                return jsonify({"error": "Deal not found"}), 404
            else:
                logger.error(f"Error updating deal_id {deal_id}: {error}")
                return jsonify({"error": "Failed to update deal"}), 500

        logger.info(
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
        logger.exception(
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
                    "based_on": seller.based_on,
                    "bank": seller.bank.name,
                    "current_account": seller.current_account,
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
        logger.exception(f"Ошибка при удалении продавца: {str(e)}")
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
    new_base_on = data.get("base_on")
    new_bank: dict = json.loads(data.get("bank")) if data.get("bank") else None
    new_current = data.get("current")

    logger.info(f"Bank: {new_bank}")

    # Вызываем функцию обновления клиента в базе данных
    response_data, status_code = update_client_in_db(
        deal_id,
        new_address,
        new_phone,
        new_email,
        new_signer,
        new_base_on,
        new_bank,
        new_current,
    )

    return jsonify(response_data), status_code


@deal_inside_bp.route("/conclusion/<deal_id>", methods=["GET"])
def conclusion(deal_id: int):
    """Страница экономического заключения сделки"""
    client = Deal.query.get(deal_id).client
    return render_template("conclusion.html", deal_id=deal_id, client=client)
