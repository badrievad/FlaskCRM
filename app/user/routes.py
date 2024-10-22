from flask import render_template, redirect, url_for, session, flash
from flask_login import login_user, logout_user, current_user

from app.user.forms import LoginForm
from app.user.models import User
from logger import logging

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
            # Проверяем, есть ли у пользователя активная сессия
            if user.active_session_id:
                flash("Пользователь с этим логином уже авторизован на сайте.", "info")
                return redirect(url_for("user.login"))

            # Авторизуем пользователя
            login_user(user, remember=form.remember_me.data)
            logging.info(f"{user.login} зашел на сайт.")

            # Сохраняем новый идентификатор сессии
            user.set_active_session()

            session["username"] = user.login

            # Перенаправляем в зависимости от роли
            if user.is_manager:
                return redirect(url_for("leas_calc.get_leasing_calculator"))
            return redirect(url_for("deal.index_crm"))
        else:
            flash("Неправильный логин или пароль", "error")
    return redirect(url_for("user.login"))


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
