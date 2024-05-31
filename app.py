from flask import (
    Flask,
    render_template,
    request,
    Blueprint,
    jsonify,
)
from flask_socketio import SocketIO
from db import db
from models import Deal

app = Flask(__name__)
app.config.from_pyfile("config.py")

db.init_app(app)
socketio = SocketIO(app)

crm_static_bp = Blueprint(
    "crm", __name__, static_folder="static", static_url_path="/crm/static"
)
app.register_blueprint(crm_static_bp)


@app.route("/crm", methods=["GET"])
def index_crm():
    deals = Deal.query.all()
    return render_template("crm.html", deals=deals)


@app.route("/crm/create_deal", methods=["POST"])
def create_deal():
    title = request.form.get("title")
    new_deal = Deal(title=title)
    db.session.add(new_deal)
    db.session.commit()
    deal_data = {"id": new_deal.id, "title": new_deal.title}
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
