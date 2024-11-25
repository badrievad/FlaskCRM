from flask import jsonify, render_template, request

from logger import logging

from ...deal.models import Deal
from ..risk_department.db_func import get_decision, process_risk_decision
from . import risk_department_bp


@risk_department_bp.route("/<int:deal_id>", methods=["GET"])
def risk_department(deal_id) -> str:
    logging.info(f"Deal ID: {deal_id}")
    client = Deal.query.get(deal_id).client
    decision = get_decision(deal_id)
    return render_template(
        "risk_department.html",
        deal_id=deal_id,
        client=client,
        decision=decision,
    )


@risk_department_bp.route("/process_decision/<int:deal_id>", methods=["POST"])
def process_decision(deal_id):
    data = request.get_json()
    decision = data.get("decision")
    logging.info(f"Deal ID: {deal_id}, Decision: {decision}")

    success, message = process_risk_decision(deal_id, decision)

    if success:
        return jsonify({"success": True, "message": message})
    else:
        # Если решение некорректно или произошла ошибка, возвращаем соответствующий статус
        status_code = 400 if message == "Некорректное решение." else 500
        return jsonify({"success": False, "message": message}), status_code
