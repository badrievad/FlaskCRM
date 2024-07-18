from flask import Blueprint

leas_calc_bp = Blueprint("leas_calc", __name__)

from . import routes  # noqa F401
