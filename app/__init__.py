from flask import Flask, Blueprint
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

socketio = SocketIO()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "user.login"

crm_static_bp = Blueprint(
    "crm", __name__, static_folder="static", static_url_path="/crm/static"
)


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config.from_pyfile("config.py")

    Migrate(app, db)

    from .deal import deal_bp as deal_blueprint
    from .user import user_bp as user_blueprint

    app.register_blueprint(crm_static_bp)
    app.register_blueprint(deal_blueprint)
    app.register_blueprint(user_blueprint)

    socketio.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    return app
