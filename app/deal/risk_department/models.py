from sqlalchemy.orm import relationship

from ... import db


class RiskDepartment(db.Model):
    __tablename__ = "risk_departments"

    id = db.Column(db.Integer, primary_key=True)
    deal_id = db.Column(db.Integer, db.ForeignKey("deals.id"), nullable=False)
    decision_time = db.Column(db.DateTime, nullable=True)
    responsible_person = db.Column(db.String(100), nullable=True)

    deal = relationship("Deal", back_populates="risk_department")
