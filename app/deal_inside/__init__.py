from flask import Blueprint

deal_inside_bp = Blueprint("deal_inside", __name__, url_prefix="/crm/deal/inside")

from . import routes, events  # noqa F401
