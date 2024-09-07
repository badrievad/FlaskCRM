from sqlalchemy.orm import joinedload

from . import deal_inside_bp
from flask import (
    jsonify,
    request,
    render_template,
)
from logger import logging
from .sql_queries import get_users_with_roles, update_deal_created_by
from ..config import suggestions_token
from ..deal.models import Deal
from .. import socketio


@deal_inside_bp.route("/<deal_id>", methods=["GET"])
def enter_into_deal(deal_id: int) -> render_template:
    # Находим сделку по deal_id
    deal: Deal = Deal.query.options(joinedload(Deal.leas_calculators)).get(deal_id)

    # Проверяем, что сделка найдена
    if not deal:
        return "Сделка не найдена", 404

    # Получаем group_id сделки
    group_id = deal.group_id

    if group_id:
        logging.info(f"Group ID: {group_id}")
        # Получаем все связанные сделки по group_id, включая текущую сделку
        related_deals = Deal.query.filter_by(group_id=group_id).all()
    else:
        logging.info("Group ID: None")
        # Если group_id пуст, возвращаем только текущую сделку
        related_deals = [deal]

    # Собираем уникальные лизинговые калькуляторы, связанные с этими сделками
    leas_calculators = []
    for related_deal in related_deals:
        for leas_calc in related_deal.leas_calculators:
            leas_calc_with_deal_info = {
                "leas_calc": leas_calc,
                "dl_number": related_deal.dl_number,  # Поля из deals
                "deal_title": related_deal.title,
                "company_inn": related_deal.company_inn,
                "created_by": related_deal.created_by,
                "created_at": related_deal.created_at,
            }
            leas_calculators.append(leas_calc_with_deal_info)
    return render_template(
        "deal.html",
        deal=deal,
        leas_calculators=leas_calculators,  # Передаем список всех связанных лизингодателей с полями из deals
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
