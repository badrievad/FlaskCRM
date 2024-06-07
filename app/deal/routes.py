import datetime

from . import deal_bp
from .. import socketio, db

from .deals_db import write_deal_to_db
from .deals_validate import DealsValidate

from flask import request, jsonify, render_template
from flask_login import current_user, login_required
from logger import logging
from app.deal.models import Deal
from app.user.models import User
from app.config import suggestions_token


@deal_bp.route("/crm/deal/create_deal", methods=["POST"])
def create_deal():
    deal: DealsValidate = DealsValidate(request.get_json())
    company_name: str = deal.get_company_name
    company_inn: str = deal.get_company_inn
    deal_data: dict = write_deal_to_db(
        company_name, company_inn, current_user.fullname, datetime.datetime.now()
    )
    logging.info(
        f"{current_user} создал новую сделку. Название сделки: {company_name}. "
        f"ID сделки: {deal_data['id']}. Дата создания: {deal_data['created_at']}."
    )
    socketio.emit("new_deal", deal_data)  # Send to all connected clients
    return jsonify(deal_data), 201


@deal_bp.route("/crm/deal/delete_deal/<int:deal_id>", methods=["POST"])
def delete_deal(deal_id):
    deal = Deal.query.get(deal_id)
    if deal:
        db.session.delete(deal)
        db.session.commit()
        socketio.emit("delete_deal", {"id": deal_id})
        return jsonify({"result": "success"}), 200
    return jsonify({"result": "error", "message": "Deal not found"}), 404


@deal_bp.route("/crm/deal/deal_to_archive/<int:deal_id>", methods=["POST"])
def deal_to_archive(deal_id):
    deal: Deal = Deal.query.get(deal_id)
    if deal:
        deal.status = "archived"
        deal.archived_at = datetime.datetime.now()
        db.session.commit()
        socketio.emit("deal_to_archive", deal.to_json())
        return jsonify({"result": "success"}), 200
    return jsonify({"result": "error", "message": "Deal not found"}), 404


@deal_bp.route("/crm/deal/deal_to_active/<int:deal_id>", methods=["POST"])
def deal_to_active(deal_id):
    """Изменить статус сделки на активную."""

    deal: Deal = Deal.query.get(deal_id)
    if deal:
        deal.status = "active"
        deal.archived_at = None
        deal.created_at = datetime.datetime.now()
        db.session.commit()
        socketio.emit("deal_to_active", deal.to_json())
        return jsonify({"result": "success"}), 200
    return jsonify({"result": "error", "message": "Deal not found"}), 404


@deal_bp.route("/crm", methods=["GET"])
@login_required
def index_crm():
    deals = Deal.query.all()
    users = User.query.all()
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
        suggestions_token=suggestions_token,
    )


@deal_bp.route("/crm/deals/active", methods=["GET"])
def get_deals_active():
    active_deals = Deal.query.filter_by(status="active").all()
    active_deals_count = len(active_deals)
    archived_deals_count = Deal.query.filter_by(status="archived").count()
    return jsonify(
        {
            "deals": [
                {
                    "id": deal.id,
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
def get_deals_archived():
    archived_deals = Deal.query.filter_by(status="archived").all()
    active_deals_count = Deal.query.filter_by(status="active").count()
    archived_deals_count = len(archived_deals)
    return jsonify(
        {
            "deals": [
                {
                    "id": deal.id,
                    "title": deal.title,
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
