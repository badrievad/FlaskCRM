from sqlalchemy.orm import relationship

from .. import db


class LeasCalculator(db.Model):
    __tablename__ = "leas_calculator"

    id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.String(150), nullable=True)
    item_year = db.Column(db.Integer, nullable=True)
    item_condition = db.Column(db.String(50), nullable=True)
    item_price = db.Column(db.Numeric(precision=10, scale=2), nullable=True)
    item_price_str = db.Column(db.String(50), nullable=True)
    item_name = db.Column(db.String(500), nullable=True)
    currency = db.Column(db.String(10), nullable=True)
    foreign_price = db.Column(db.Numeric(precision=10, scale=2), nullable=True)
    foreign_price_str = db.Column(db.String(50), nullable=True)
    initial_payment = db.Column(db.Numeric(precision=10, scale=2), nullable=True)
    initial_payment_str = db.Column(db.String(50), nullable=True)
    initial_payment_percent = db.Column(db.Float, nullable=True)
    credit_sum = db.Column(db.Numeric(precision=10, scale=2), nullable=True)
    credit_sum_str = db.Column(db.String(50), nullable=True)
    credit_sum_percent = db.Column(db.Float, nullable=True)
    credit_term = db.Column(db.Integer, nullable=True)
    bank_commission = db.Column(db.Float, nullable=True)
    lkmb_commission = db.Column(db.Float, nullable=True)
    insurance_casko = db.Column(db.Float, nullable=True)
    insurance_osago = db.Column(db.Float, nullable=True)
    health_insurance = db.Column(db.Float, nullable=True)
    health_insurance_str = db.Column(db.String(50), nullable=True)
    other_insurance = db.Column(db.Float, nullable=True)
    other_insurance_str = db.Column(db.String(50), nullable=True)
    agent_commission = db.Column(db.Float, nullable=True)
    manager_bonus = db.Column(db.Float, nullable=True)
    tracker = db.Column(db.Float, nullable=True)
    tracker_str = db.Column(db.String(50), nullable=True)
    mayak = db.Column(db.Float, nullable=True)
    mayak_str = db.Column(db.String(50), nullable=True)
    fedresurs = db.Column(db.Float, nullable=True)
    fedresurs_str = db.Column(db.String(50), nullable=True)
    gsm = db.Column(db.Float, nullable=True)
    gsm_str = db.Column(db.String(50), nullable=True)
    mail = db.Column(db.Float, nullable=True)
    mail_str = db.Column(db.String(50), nullable=True)
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
    deal = relationship("Deal", back_populates="leas_calculators")

    def to_dict(self):
        return {
            "id": self.id,
            "item_type": self.item_type,
            "item_year": self.item_year,
            "item_condition": self.item_condition,
            "item_price": self.item_price,
            "item_price_str": self.item_price_str,
            "item_name": self.item_name,
            "currency": self.currency,
            "foreign_price": self.foreign_price,
            "foreign_price_str": self.foreign_price_str,
            "initial_payment": self.initial_payment,
            "initial_payment_str": self.initial_payment_str,
            "initial_payment_percent": self.initial_payment_percent,
            "credit_sum": self.credit_sum,
            "credit_sum_str": self.credit_sum_str,
            "credit_sum_percent": self.credit_sum_percent,
            "credit_term": self.credit_term,
            "bank_commission": self.bank_commission,
            "lkmb_commission": self.lkmb_commission,
            "insurance_casko": self.insurance_casko,
            "insurance_osago": self.insurance_osago,
            "health_insurance": self.health_insurance,
            "health_insurance_str": self.health_insurance_str,
            "other_insurance": self.other_insurance,
            "other_insurance_str": self.other_insurance_str,
            "agent_commission": self.agent_commission,
            "manager_bonus": self.manager_bonus,
            "tracker": self.tracker,
            "tracker_str": self.tracker_str,
            "mayak": self.mayak,
            "mayak_str": self.mayak_str,
            "fedresurs": self.fedresurs,
            "fedresurs_str": self.fedresurs_str,
            "gsm": self.gsm,
            "gsm_str": self.gsm_str,
            "mail": self.mail,
            "mail_str": self.mail_str,
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

    def to_dict(self):
        return {
            "id": self.id,
            "tranche_1_size": self.tranche_1_size,
            "tranche_1_rate": self.tranche_1_rate,
            "tranche_1_fee": self.tranche_1_fee,
            "tranche_1_own_fee": self.tranche_1_own_fee,
            "tranche_1_credit_date": self.tranche_1_credit_date,
            "tranche_1_payment_date": self.tranche_1_payment_date,
            "tranche_2_size": self.tranche_2_size,
            "tranche_2_rate": self.tranche_2_rate,
            "tranche_2_fee": self.tranche_2_fee,
            "tranche_2_own_fee": self.tranche_2_own_fee,
            "tranche_2_credit_date": self.tranche_2_credit_date,
            "tranche_2_payment_date": self.tranche_2_payment_date,
            "tranche_3_size": self.tranche_3_size,
            "tranche_3_rate": self.tranche_3_rate,
            "tranche_3_fee": self.tranche_3_fee,
            "tranche_3_own_fee": self.tranche_3_own_fee,
            "tranche_3_credit_date": self.tranche_3_credit_date,
            "tranche_3_payment_date": self.tranche_3_payment_date,
            "tranche_4_size": self.tranche_4_size,
            "tranche_4_rate": self.tranche_4_rate,
            "tranche_4_fee": self.tranche_4_fee,
            "tranche_4_own_fee": self.tranche_4_own_fee,
            "tranche_4_credit_date": self.tranche_4_credit_date,
            "tranche_4_payment_date": self.tranche_4_payment_date,
            "tranche_5_size": self.tranche_5_size,
            "tranche_5_rate": self.tranche_5_rate,
            "tranche_5_fee": self.tranche_5_fee,
            "tranche_5_own_fee": self.tranche_5_own_fee,
            "tranche_5_credit_date": self.tranche_5_credit_date,
            "tranche_5_payment_date": self.tranche_5_payment_date,
        }


class LeasingItem(db.Model):
    """Модель для автоподсказок по имени предмета лизинга"""

    __tablename__ = "leas_items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
