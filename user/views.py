from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user

from user.forms import LoginForm
from user.models import User
from logger import logging

blueprint = Blueprint("user", __name__, url_prefix="/crm/users")


@blueprint.route("/login")
def login():
    login_form = LoginForm()
    return render_template("login_page.html", form=login_form)


def agree():
    return redirect()


@blueprint.route("/process-login", methods=["POST"])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Вы вошли на сайт", "success")
            logging.info(f"{current_user} зашел на сайт.")
            return redirect(url_for("index_crm"))
    flash("Неправильное имя пользователя или пароль", "info")
    return redirect(url_for("user.login"))


@blueprint.route("/logout")
def exit_user():
    logout_user()
    return redirect(url_for("user.login"))
