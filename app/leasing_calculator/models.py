from sqlalchemy.orm import relationship

from .. import db


class LeasCalculator(db.Model):
    __tablename__ = "leas_calculator"

    id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.String(150), nullable=True)
    item_price = db.Column(db.Numeric(precision=10, scale=2), nullable=True)
    item_price_str = db.Column(db.String(50), nullable=True)
    item_name = db.Column(db.String(500), nullable=True)
    currency = db.Column(db.String(10), nullable=True)
    foreign_price = db.Column(db.Numeric(precision=10, scale=2), nullable=True)
    initial_payment = db.Column(db.Numeric(precision=10, scale=2), nullable=True)
    credit_sum = db.Column(db.Numeric(precision=10, scale=2), nullable=True)
    credit_term = db.Column(db.Integer, nullable=True)
    bank_commission = db.Column(db.Float, nullable=True)
    insurance_casko = db.Column(db.Float, nullable=True)
    insurance_osago = db.Column(db.Float, nullable=True)
    health_insurance = db.Column(db.Float, nullable=True)
    other_insurance = db.Column(db.Float, nullable=True)
    agent_commission = db.Column(db.Float, nullable=True)
    manager_bonus = db.Column(db.Float, nullable=True)
    tracker = db.Column(db.Float, nullable=True)
    mayak = db.Column(db.Float, nullable=True)
    fedresurs = db.Column(db.Float, nullable=True)
    gsm = db.Column(db.Float, nullable=True)
    mail = db.Column(db.Float, nullable=True)
    input_period = db.Column(db.Date, nullable=True)
    trance_id = db.Column(db.Integer, db.ForeignKey("tranches.id"), nullable=True)

    date = db.Column(db.Date, nullable=False)
    date_ru = db.Column(db.String(50), nullable=True)
    path_to_file = db.Column(db.String(500), nullable=True)
    manager_login = db.Column(db.String(200), nullable=False)
    title = db.Column(
        db.String(200), nullable=True
    )  # Название xlsx файла (для скачивания)
    deal_id = db.Column(db.Integer, db.ForeignKey("deals.id"), nullable=True)

    tranche = relationship("Tranches", back_populates="leas_calculator", uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            "item_type": self.item_type,
            "item_price": self.item_price,
            "item_price_str": self.item_price_str,
            "item_name": self.item_name,
            "currency": self.currency,
            "foreign_price": self.foreign_price,
            "initial_payment": self.initial_payment,
            "credit_sum": self.credit_sum,
            "credit_term": self.credit_term,
            "bank_commission": self.bank_commission,
            "insurance_casko": self.insurance_casko,
            "insurance_osago": self.insurance_osago,
            "health_insurance": self.health_insurance,
            "other_insurance": self.other_insurance,
            "agent_commission": self.agent_commission,
            "manager_bonus": self.manager_bonus,
            "tracker": self.tracker,
            "mayak": self.mayak,
            "fedresurs": self.fedresurs,
            "gsm": self.gsm,
            "mail": self.mail,
            "input_period": self.input_period,
            "trance_id": self.trance_id,
            "date": self.date,
            "date_ru": self.date_ru,
            "path_to_file": self.path_to_file,
            "manager_login": self.manager_login,
            "title": self.title,
            "deal_id": self.deal_id,
        }


class Tranches(db.Model):
    __tablename__ = "tranches"

    id = db.Column(db.Integer, primary_key=True)
    tranche_1_size = db.Column(db.Float, nullable=True)
    tranche_1_rate = db.Column(db.Float, nullable=True)
    tranche_1_fee = db.Column(db.Float, nullable=True)
    tranche_1_own_fee = db.Column(db.Float, nullable=True)
    tranche_1_credit_date = db.Column(db.Date, nullable=True)
    tranche_1_payment_date = db.Column(db.Date, nullable=True)
    tranche_2_size = db.Column(db.Float, nullable=True)
    tranche_2_rate = db.Column(db.Float, nullable=True)
    tranche_2_fee = db.Column(db.Float, nullable=True)
    tranche_2_own_fee = db.Column(db.Float, nullable=True)
    tranche_2_credit_date = db.Column(db.Date, nullable=True)
    tranche_2_payment_date = db.Column(db.Date, nullable=True)
    tranche_3_size = db.Column(db.Float, nullable=True)
    tranche_3_rate = db.Column(db.Float, nullable=True)
    tranche_3_fee = db.Column(db.Float, nullable=True)
    tranche_3_own_fee = db.Column(db.Float, nullable=True)
    tranche_3_credit_date = db.Column(db.Date, nullable=True)
    tranche_3_payment_date = db.Column(db.Date, nullable=True)
    tranche_4_size = db.Column(db.Float, nullable=True)
    tranche_4_rate = db.Column(db.Float, nullable=True)
    tranche_4_fee = db.Column(db.Float, nullable=True)
    tranche_4_own_fee = db.Column(db.Float, nullable=True)
    tranche_4_credit_date = db.Column(db.Date, nullable=True)
    tranche_4_payment_date = db.Column(db.Date, nullable=True)
    tranche_5_size = db.Column(db.Float, nullable=True)
    tranche_5_rate = db.Column(db.Float, nullable=True)
    tranche_5_fee = db.Column(db.Float, nullable=True)
    tranche_5_own_fee = db.Column(db.Float, nullable=True)
    tranche_5_credit_date = db.Column(db.Date, nullable=True)
    tranche_5_payment_date = db.Column(db.Date, nullable=True)

    leas_calculator = relationship(
        "LeasCalculator", back_populates="tranche", uselist=False
    )


class LeasingItem(db.Model):
    """Модель для автоподсказок по имени предмета лизинга"""

    __tablename__ = "leas_items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
