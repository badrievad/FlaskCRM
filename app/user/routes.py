from flask import render_template, redirect, url_for, session, request
from flask_login import login_user, logout_user, current_user

from app.user.forms import LoginForm
from app.user.models import User

from . import user_bp
from .. import login_manager


@user_bp.route("/crm/user/login")
def login():
    login_form = LoginForm()
    return render_template("login_page.html", form=login_form)


@user_bp.route("/crm/user/process-login", methods=["POST"])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.username.data).first()
        if user and user.check_password(form.password.data):
            # Проверка на наличие активной сессии
            if user.active_session_id and not request.args.get("force"):
                # Отправляем информацию для показа модального окна
                return {"status": "active_session"}

            # Если force=True, завершаем старую сессию и входим с новой
            login_user(user, remember=form.remember_me.data)
            user.set_active_session()  # Установка новой активной сессии
            session["username"] = user.login
            session["session_id"] = user.active_session_id

            redirect_url = (
                url_for("leas_calc.get_leasing_calculator")
                if user.is_manager
                else url_for("deal.index_crm")
            )
            return {"status": "success", "redirect_url": redirect_url}

        else:
            return {"status": "error", "message": "Неправильный логин или пароль"}
    return {"status": "error", "message": "Форма не прошла валидацию"}


@user_bp.route("/crm/user/logout")
def exit_user():
    if current_user.is_authenticated:
        # Очищаем активную сессию
        current_user.clear_active_session()

    logout_user()
    session.pop("username", None)
    return redirect(url_for("user.login"))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
