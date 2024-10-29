from functools import wraps

from flask import current_app, flash, request, redirect, url_for, session
from flask_login import config, current_user, logout_user

from app.user.models import User


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


def validate_active_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            # Retrieve session ID from DB and match with the active session
            user = User.query.get(current_user.id)
            if user.active_session_id != session.get("session_id"):
                flash(
                    "Ваша сессия больше не действительна. Пожалуйста, войдите снова.",
                    "info",
                )
                logout_user()  # Logout invalid session
                return redirect(url_for("user.login"))
        return f(*args, **kwargs)

    return decorated_function
