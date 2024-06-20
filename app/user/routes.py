from flask import flash, render_template, redirect, url_for, session
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
            login_user(user, remember=form.remember_me.data)
            flash("Вы вошли на сайт", "success")
            logging.info(f"{current_user} зашел на сайт.")
            session["username"] = current_user.login  # Устанавливаем username в сессию
            return redirect(url_for("deal.index_crm"))
    flash("Неправильное имя пользователя или пароль", "info")
    return redirect(url_for("user.login"))


@user_bp.route("/crm/user/logout")
def exit_user():
    logout_user()
    session.pop("username", None)
    return redirect(url_for("user.login"))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
