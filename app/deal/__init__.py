from flask import Blueprint

deal_bp = Blueprint("deal", __name__)

from . import routes, events
