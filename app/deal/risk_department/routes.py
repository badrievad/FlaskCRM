from flask import render_template

from logger import logging

from ...deal.models import Deal
from . import risk_department_bp


@risk_department_bp.route("/<int:deal_id>", methods=["GET"])
def risk_department(deal_id) -> str:
    logging.info(f"Deal ID: {deal_id}")
    client = Deal.query.get(deal_id).client
    return render_template("risk_department.html", deal_id=deal_id, client=client)
