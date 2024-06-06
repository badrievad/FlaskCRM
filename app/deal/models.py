from .. import db


class DealSteps(db.Model):
    __tablename__ = "deal_steps"

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
    __tablename__ = "deals"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company_inn = db.Column(db.String(20), nullable=False)
    created_by = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    archived_at = db.Column(db.DateTime, nullable=True)

    def to_json(self) -> dict:
        if self.archived_at is None:
            archived_at = ""
        else:
            archived_at = self.archived_at.strftime("%d.%m.%Y %H:%M:%S")
        return {
            "id": self.id,
            "title": self.title,
            "company_inn": self.company_inn,
            "created_by": self.created_by,
            "created_at": self.created_at.strftime("%d.%m.%Y %H:%M:%S"),
            "archived_at": archived_at,
        }
