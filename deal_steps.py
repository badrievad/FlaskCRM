from app import app, socketio
from db import db
from flask import render_template, request, session, redirect, url_for
from flask_socketio import emit
from models import DealSteps
from datetime import datetime


@app.route("/crm/<int:deal_id>", methods=["GET", "POST"])
def deal_steps():
    deal = DealSteps.query.first()
    return render_template("steps.html", deal=deal)


@app.route("/crm/<int:deal_id>/set_user", methods=["POST"])
def set_user():
    session["username"] = request.form["username"]
    session["position"] = request.form["position"]
    deal = DealSteps.query.first()
    if not deal:
        deal = DealSteps()
        db.session.add(deal)
        db.session.commit()
    return redirect(url_for("index"))


@socketio.on("approve_step")
def approve_step(data):
    step = data["step"]
    username = session.get("username", "Anonymous")
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    deal = DealSteps.query.first()

    if step == "step1":
        deal.step1_approved = True
        deal.step1_time = time_now
        deal.step1_user = username
    elif step == "step2":
        deal.step2_approved = True
        deal.step2_time = time_now
        deal.step2_user = username

    if deal.step1_approved and deal.step2_approved:
        deal.step3_approved = True
        deal.step3_time = time_now
        deal.step3_user = username

    db.session.commit()

    emit(
        "update_steps",
        {
            "step1": {
                "approved": deal.step1_approved,
                "time": deal.step1_time,
                "user": deal.step1_user,
            },
            "step2": {
                "approved": deal.step2_approved,
                "time": deal.step2_time,
                "user": deal.step2_user,
            },
            "step3": {
                "approved": deal.step3_approved,
                "time": deal.step3_time,
                "user": deal.step3_user,
            },
        },
        broadcast=True,
    )


@socketio.on("revoke_step")
def revoke_step(data):
    step = data["step"]
    deal = DealSteps.query.first()

    if step == "step1":
        deal.step1_approved = False
        deal.step1_time = None
        deal.step1_user = None
    elif step == "step2":
        deal.step2_approved = False
        deal.step2_time = None
        deal.step2_user = None

    if not deal.step1_approved or not deal.step2_approved:
        deal.step3_approved = False
        deal.step3_time = None
        deal.step3_user = None

        db.session.commit()

        emit(
            "update_steps",
            {
                "step1": {
                    "approved": deal.step1_approved,
                    "time": deal.step1_time,
                    "user": deal.step1_user,
                },
                "step2": {
                    "approved": deal.step2_approved,
                    "time": deal.step2_time,
                    "user": deal.step2_user,
                },
                "step3": {
                    "approved": deal.step3_approved,
                    "time": deal.step3_time,
                    "user": deal.step3_user,
                },
            },
            broadcast=True,
        )

    db.session.commit()
