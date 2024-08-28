from functools import wraps

from flask import current_app, flash, request, redirect, url_for
from flask_login import config, current_user


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in config.EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get("LOGIN_DISABLED"):
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not current_user.is_admin:
            flash("Эта страница доступна только админам", "info")
            if current_user.is_manager:
                return redirect(url_for("manager.bki_page"))
            if current_user.is_risk:
                return redirect(url_for("risk.risk_page"))
            if current_user.is_tester:
                return redirect(url_for("risk.risk_page"))
        return func(*args, **kwargs)

    return decorated_view


def _tester_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in config.EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get("LOGIN_DISABLED"):
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not current_user.is_tester:
            if current_user.is_manager:
                flash("Эта страница доступна только админам и тестировщикам", "info")
                return redirect(url_for("leas_calc.get_leasing_calculator"))
        return func(*args, **kwargs)

    return decorated_view
