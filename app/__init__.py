from flask import Flask, Blueprint
from flask_caching import Cache
from flask_migrate import Migrate  # type: ignore
from flask_socketio import SocketIO  # type: ignore
from flask_login import LoginManager  # type: ignore
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # type: ignore

from .celery_utils import celery_init_app
from .config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

cache = Cache()
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
    CORS(app)
    app.debug = debug
    app.config.from_pyfile("config.py")

    app.config.update(
        CELERY={
            "broker_url": CELERY_BROKER_URL,
            "result_backend": CELERY_RESULT_BACKEND,
            "task_ignore_result": True,
            "broker_connection_retry_on_startup": True,
        },
    )

    Migrate(app, db)

    from .deal import deal_bp as deal_blueprint
    from .user import user_bp as user_blueprint
    from .leasing_calculator import leas_calc_bp as leas_calc_blueprint
    from .deal_inside import deal_inside_bp as deal_inside_blueprint

    app.register_blueprint(crm_static_bp)
    app.register_blueprint(deal_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(leas_calc_blueprint)
    app.register_blueprint(deal_inside_blueprint)

    cache.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    db.init_app(app)
    login_manager.init_app(app)
    celery_init_app(app)

    return app
