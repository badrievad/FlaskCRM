from flask import jsonify, redirect, render_template, request, url_for

from logger import logging

from ...deal.models import Deal
from . import risk_department_bp


@risk_department_bp.route("/<int:deal_id>", methods=["GET"])
def risk_department(deal_id) -> str:
    logging.info(f"Deal ID: {deal_id}")
    client = Deal.query.get(deal_id).client
    return render_template("risk_department.html", deal_id=deal_id, client=client)


@risk_department_bp.route("/process_decision/<int:deal_id>", methods=["POST"])
def process_decision(deal_id):
    data = request.get_json()
    decision = data.get("decision")
    logging.info(f"Deal ID: {deal_id}, Decision: {decision}")

    if decision == "approve":
        # Логика для одобрения сделки
        message = "Сделка одобрена."
    elif decision == "send_to_committee":
        # Логика для отправки на инвестиционный комитет
        message = "Сделка отправлена на инвестиционный комитет."
    elif decision == "reject":
        # Логика для отказа по сделке
        message = "По сделке отказано."
    else:
        # Обработка неверного решения
        return jsonify({"success": False, "message": "Некорректное решение."}), 400

    # Выполняем необходимые действия с базой данных
    # ...

    return jsonify({"success": True, "message": message})
