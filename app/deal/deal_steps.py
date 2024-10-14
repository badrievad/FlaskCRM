# from . import deal_bp
# from .. import db
#
# from flask import render_template, request, session, redirect, url_for
# from models import DealSteps
#
#
# @deal_bp.route("/crm/<int:deal_id>", methods=["GET", "POST"])
# def deal_steps():
#     deal = DealSteps.query.first()
#     return render_template("steps.html", deal=deal)
#
#
# @deal_bp.route("/crm/<int:deal_id>/set_user", methods=["POST"])
# def set_user():
#     session["username"] = request.form["username"]
#     session["position"] = request.form["position"]
#     deal = DealSteps.query.first()
#     if not deal:
#         deal = DealSteps()
#         db.session.add(deal)
#         db.session.commit()
#     return redirect(url_for("index"))
