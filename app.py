import datetime

from flask import (
    Flask,
    render_template,
    request,
    Blueprint,
    jsonify,
)
from flask_login import LoginManager, login_required, current_user
from flask_socketio import SocketIO
from flask_migrate import Migrate
from db import db

from logger import logging
from models import Deal
from user.models import User

from user.views import blueprint as user_blueprint

app = Flask(__name__)
app.config.from_pyfile("config.py")

db.init_app(app)
socketio = SocketIO(app)
migrate = Migrate(app, db)

crm_static_bp = Blueprint(
    "crm", __name__, static_folder="static", static_url_path="/crm/static"
)
app.register_blueprint(crm_static_bp)
app.register_blueprint(user_blueprint)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/crm", methods=["GET"])
@login_required
def index_crm():
    #  TODO: Нужно сделать, чтобы не только Title (название компании) выводился на странице CRM, но и остальные данные.
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
    )


@app.route("/crm/create_deal", methods=["POST"])
def create_deal():
    company_name = request.form.get("title")
    new_deal = Deal(
        title=company_name,
        company_inn="1234567890",
        created_by=current_user.fullname,
        created_at=datetime.datetime.now(),
    )
    db.session.add(new_deal)
    db.session.commit()
    deal_data = new_deal.to_json()
    logging.info(
        f"{current_user} создал новую сделку. Название сделки: {company_name}. "
        f"ID сделки: {new_deal.id}. Дата создания: {new_deal.created_at}."
    )
    socketio.emit("new_deal", deal_data)  # Send to all connected clients
    return jsonify(deal_data), 201


@app.route("/crm/delete_deal/<int:deal_id>", methods=["POST"])
def delete_deal(deal_id):
    deal = Deal.query.get(deal_id)
    if deal:
        db.session.delete(deal)
        db.session.commit()
        socketio.emit("delete_deal", {"id": deal_id})
        return jsonify({"result": "success"}), 200
    return jsonify({"result": "error", "message": "Deal not found"}), 404
