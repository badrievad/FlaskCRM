from flask import Blueprint

client_application_bp = Blueprint("client_application", __name__, url_prefix="/client")

from . import routes  # noqa
