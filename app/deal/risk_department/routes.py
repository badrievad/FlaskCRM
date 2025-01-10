from flask import jsonify, render_template, request

from log_conf import logger

from ... import socketio
from ...deal.models import Deal
from ..risk_department.db_func import (
    delete_risk_decision,
    get_decision,
    process_risk_decision,
)
from ..risk_department.other_utils import format_russian_date
from . import risk_department_bp


@risk_department_bp.route("/<int:deal_id>", methods=["GET"])
def risk_department(deal_id) -> str:
    logger.info(f"Deal ID: {deal_id}")
    client = Deal.query.get(deal_id).client

    # Получаем group_id основной сделки
    deal: Deal = Deal.query.get(deal_id)
    group_id = deal.group_id
    if group_id:
        related_deals = Deal.query.filter_by(group_id=group_id).all()
    else:
        related_deals = Deal.query.filter_by(id=deal_id).all()

    sellers: dict = {}
    try:
        for i, leas_calculator in enumerate(
            leas_calculator
            for related_deal in related_deals
            for leas_calculator in related_deal.leas_calculators
        ):
            sellers[f"Продавец {i + 1}"] = {
                "name": leas_calculator.seller.name,
                "inn": leas_calculator.seller.inn,
                "date_of_registration": format_russian_date(
                    leas_calculator.seller.date_of_registration
                ),
                "address": leas_calculator.seller.address,
                "item_name": leas_calculator.item_name,
                "item_year": leas_calculator.item_year,
                "item_price": leas_calculator.item_price_str,
                "item_type": leas_calculator.item_type,
            }
    except Exception as ex:
        logger.error(ex)

    logger.info(f"Sellers: {sellers}")
    decision = get_decision(deal_id)

    folder_path = deal.deal_path

    return render_template(
        "risk_department.html",
        deal_id=deal_id,
        client=client,
        decision=decision,
        sellers=sellers,
        folder_path=folder_path,
    )


@risk_department_bp.route("/process_decision/<int:deal_id>", methods=["POST"])
def process_decision(deal_id):
    data = request.get_json()
    decision = data.get("decision")
    logger.info(f"Deal ID: {deal_id}, Decision: {decision}")

    success, message = process_risk_decision(deal_id, decision)

    if success:
        socketio.emit(
            "decision_update",
            {"deal_id": deal_id, "decision": decision},
        )
        return jsonify({"success": True, "message": message})
    else:
        # Если решение некорректно или произошла ошибка, возвращаем соответствующий статус
        status_code = 400 if message == "Некорректное решение." else 500
        return jsonify({"success": False, "message": message}), status_code


@risk_department_bp.route("/delete_decision/<int:deal_id>", methods=["DELETE"])
def delete_decision(deal_id):
    logger.info(f"Удаление решения для сделки с ID: {deal_id}")

    success, message = delete_risk_decision(deal_id)

    if success:
        socketio.emit("decision_update", {"deal_id": deal_id, "decision": None})
        return jsonify({"success": True, "message": message})
    else:
        status_code = 404 if message == "Решение не найдено." else 500
        return jsonify({"success": False, "message": message}), status_code
