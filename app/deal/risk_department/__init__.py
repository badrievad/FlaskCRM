from flask import Blueprint

risk_department_bp = Blueprint(
    "risk_department", __name__, url_prefix="/crm/deal/inside/risk-department"
)

from . import routes, models  # noqa F401
