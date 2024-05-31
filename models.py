from db import db


class DealSteps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step1_approved = db.Column(db.Boolean, default=False)
    step1_time = db.Column(db.String(50))
    step1_user = db.Column(db.String(50))
    step2_approved = db.Column(db.Boolean, default=False)
    step2_time = db.Column(db.String(50))
    step2_user = db.Column(db.String(50))
    step3_approved = db.Column(db.Boolean, default=False)
    step3_time = db.Column(db.String(50))
    step3_user = db.Column(db.String(50))


class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
