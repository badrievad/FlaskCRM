from sqlalchemy.orm import relationship

from .. import db


class LeasCalculator(db.Model):
    __tablename__ = "leas_calculator"

    id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.String(150), nullable=True)
    item_year = db.Column(db.Integer, nullable=True)
    item_condition = db.Column(db.String(50), nullable=True)
    item_price = db.Column(db.Float, nullable=True)
    item_price_str = db.Column(db.String(50), nullable=True)
    item_name = db.Column(db.String(500), nullable=True)
    currency = db.Column(db.String(10), nullable=True)
    foreign_price = db.Column(db.Float, nullable=True)
    foreign_price_str = db.Column(db.String(50), nullable=True)
    initial_payment = db.Column(db.Float, nullable=True)
    initial_payment_str = db.Column(db.String(50), nullable=True)
    initial_payment_percent = db.Column(db.Float, nullable=True)
    credit_sum = db.Column(db.Float, nullable=True)
    credit_sum_str = db.Column(db.String(50), nullable=True)
    credit_sum_percent = db.Column(db.Float, nullable=True)
    credit_term = db.Column(db.Integer, nullable=True)
    bank_commission = db.Column(db.Float, nullable=True)
    lkmb_commission = db.Column(db.Float, nullable=True)
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
    depr_transport = db.Column(db.Float, nullable=True)
    depr_transport_str = db.Column(db.String(50), nullable=True)
    travel = db.Column(db.Float, nullable=True)
    travel_str = db.Column(db.String(50), nullable=True)
    stationery = db.Column(db.Float, nullable=True)
    stationery_str = db.Column(db.String(50), nullable=True)
    internet = db.Column(db.Float, nullable=True)
    internet_str = db.Column(db.String(50), nullable=True)
    pledge = db.Column(db.Float, nullable=True)
    pledge_str = db.Column(db.String(50), nullable=True)
    bank_pledge = db.Column(db.Float, nullable=True)
    bank_pledge_str = db.Column(db.String(50), nullable=True)
    express = db.Column(db.Float, nullable=True)
    express_str = db.Column(db.String(50), nullable=True)
    egrn = db.Column(db.Float, nullable=True)
    egrn_str = db.Column(db.String(50), nullable=True)
    egrul = db.Column(db.Float, nullable=True)
    egrul_str = db.Column(db.String(50), nullable=True)
    input_period = db.Column(db.Date, nullable=True)
    allocate_vat = db.Column(db.String(50), nullable=True)
    allocate_deposit = db.Column(db.String(50), nullable=True)
    allocate_redemption = db.Column(db.String(50), nullable=True)

    insurance_id = db.Column(db.Integer, db.ForeignKey("insurances.id"), nullable=True)
    trance_id = db.Column(db.Integer, db.ForeignKey("tranches.id"), nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey("sellers.id"), nullable=True)

    date = db.Column(db.Date, nullable=False)
    date_ru = db.Column(db.String(50), nullable=True)
    path_to_xlsx = db.Column(db.String(500), nullable=True)
    path_to_pdf = db.Column(db.String(500), nullable=True)
    manager_login = db.Column(db.String(200), nullable=False)
    title = db.Column(
        db.String(200), nullable=True
    )  # Название xlsx файла (для скачивания)
    deal_id = db.Column(db.Integer, db.ForeignKey("deals.id"), nullable=True)

    tranche = relationship(
        "Tranches",
        back_populates="leas_calculator",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True,
    )
    insurance = relationship(
        "Insurances",
        back_populates="leas_calculator",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True,
    )
    deal = relationship("Deal", back_populates="leas_calculators")

    # Связь с графиками платежей
    payment_schedules = relationship(
        "CalculateResultSchedule",
        back_populates="leas_calculator",
        cascade="all, delete-orphan",
    )

    seller = relationship("Seller", back_populates="leas_calculators")

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
            "depr_transport": self.depr_transport,
            "depr_transport_str": self.depr_transport_str,
            "travel": self.travel,
            "travel_str": self.travel_str,
            "stationery": self.stationery,
            "stationery_str": self.stationery_str,
            "internet": self.internet,
            "internet_str": self.internet_str,
            "pledge": self.pledge,
            "pledge_str": self.pledge_str,
            "bank_pledge": self.bank_pledge,
            "bank_pledge_str": self.bank_pledge_str,
            "express": self.express,
            "express_str": self.express_str,
            "egrn": self.egrn,
            "egrn_str": self.egrn_str,
            "egrul": self.egrul,
            "egrul_str": self.egrul_str,
            "input_period": self.input_period,
            "trance_id": self.trance_id,
            "date": self.date,
            "date_ru": self.date_ru,
            "path_to_xlsx": self.path_to_xlsx,
            "path_to_pdf": self.path_to_pdf,
            "manager_login": self.manager_login,
            "title": self.title,
            "deal_id": self.deal_id,
            "allocate_vat": self.allocate_vat,
            "allocate_deposit": self.allocate_deposit,
            "allocate_redemption": self.allocate_redemption,
        }


class Tranches(db.Model):
    __tablename__ = "tranches"

    id = db.Column(db.Integer, primary_key=True)
    tranche_1_size = db.Column(db.Float, nullable=True)
    tranche_1_rate = db.Column(db.Float, nullable=True)
    tranche_1_fee = db.Column(db.Float, nullable=True)
    tranche_1_own_fee = db.Column(db.Float, nullable=True)
    tranche_1_credit_date = db.Column(db.Date, nullable=True)
    tranche_2_size = db.Column(db.Float, nullable=True)
    tranche_2_rate = db.Column(db.Float, nullable=True)
    tranche_2_fee = db.Column(db.Float, nullable=True)
    tranche_2_own_fee = db.Column(db.Float, nullable=True)
    tranche_2_credit_date = db.Column(db.Date, nullable=True)
    tranche_3_size = db.Column(db.Float, nullable=True)
    tranche_3_rate = db.Column(db.Float, nullable=True)
    tranche_3_fee = db.Column(db.Float, nullable=True)
    tranche_3_own_fee = db.Column(db.Float, nullable=True)
    tranche_3_credit_date = db.Column(db.Date, nullable=True)
    tranche_4_size = db.Column(db.Float, nullable=True)
    tranche_4_rate = db.Column(db.Float, nullable=True)
    tranche_4_fee = db.Column(db.Float, nullable=True)
    tranche_4_own_fee = db.Column(db.Float, nullable=True)
    tranche_4_credit_date = db.Column(db.Date, nullable=True)
    tranche_5_size = db.Column(db.Float, nullable=True)
    tranche_5_rate = db.Column(db.Float, nullable=True)
    tranche_5_fee = db.Column(db.Float, nullable=True)
    tranche_5_own_fee = db.Column(db.Float, nullable=True)
    tranche_5_credit_date = db.Column(db.Date, nullable=True)

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
            "tranche_2_size": self.tranche_2_size,
            "tranche_2_rate": self.tranche_2_rate,
            "tranche_2_fee": self.tranche_2_fee,
            "tranche_2_own_fee": self.tranche_2_own_fee,
            "tranche_2_credit_date": self.tranche_2_credit_date,
            "tranche_3_size": self.tranche_3_size,
            "tranche_3_rate": self.tranche_3_rate,
            "tranche_3_fee": self.tranche_3_fee,
            "tranche_3_own_fee": self.tranche_3_own_fee,
            "tranche_3_credit_date": self.tranche_3_credit_date,
            "tranche_4_size": self.tranche_4_size,
            "tranche_4_rate": self.tranche_4_rate,
            "tranche_4_fee": self.tranche_4_fee,
            "tranche_4_own_fee": self.tranche_4_own_fee,
            "tranche_4_credit_date": self.tranche_4_credit_date,
            "tranche_5_size": self.tranche_5_size,
            "tranche_5_rate": self.tranche_5_rate,
            "tranche_5_fee": self.tranche_5_fee,
            "tranche_5_own_fee": self.tranche_5_own_fee,
            "tranche_5_credit_date": self.tranche_5_credit_date,
        }


class Insurances(db.Model):
    __tablename__ = "insurances"

    id = db.Column(db.Integer, primary_key=True)
    insurance_casko1 = db.Column(db.Float, nullable=True)
    insurance_casko2 = db.Column(db.Float, nullable=True)
    insurance_casko3 = db.Column(db.Float, nullable=True)
    insurance_casko4 = db.Column(db.Float, nullable=True)
    insurance_casko5 = db.Column(db.Float, nullable=True)
    insurance_osago1 = db.Column(db.Float, nullable=True)
    insurance_osago2 = db.Column(db.Float, nullable=True)
    insurance_osago3 = db.Column(db.Float, nullable=True)
    insurance_osago4 = db.Column(db.Float, nullable=True)
    insurance_osago5 = db.Column(db.Float, nullable=True)
    health_insurance1 = db.Column(db.Float, nullable=True)
    health_insurance1_str = db.Column(db.String(255), nullable=True)
    health_insurance2 = db.Column(db.Float, nullable=True)
    health_insurance2_str = db.Column(db.String(255), nullable=True)
    health_insurance3 = db.Column(db.Float, nullable=True)
    health_insurance3_str = db.Column(db.String(255), nullable=True)
    health_insurance4 = db.Column(db.Float, nullable=True)
    health_insurance4_str = db.Column(db.String(255), nullable=True)
    health_insurance5 = db.Column(db.Float, nullable=True)
    health_insurance5_str = db.Column(db.String(255), nullable=True)
    other_insurance1 = db.Column(db.Float, nullable=True)
    other_insurance1_str = db.Column(db.String(255), nullable=True)
    other_insurance2 = db.Column(db.Float, nullable=True)
    other_insurance2_str = db.Column(db.String(255), nullable=True)
    other_insurance3 = db.Column(db.Float, nullable=True)
    other_insurance3_str = db.Column(db.String(255), nullable=True)
    other_insurance4 = db.Column(db.Float, nullable=True)
    other_insurance4_str = db.Column(db.String(255), nullable=True)
    other_insurance5 = db.Column(db.Float, nullable=True)
    other_insurance5_str = db.Column(db.String(255), nullable=True)

    leas_calculator = relationship(
        "LeasCalculator", back_populates="insurance", uselist=False
    )

    def to_dict(self):
        return {
            "insurance_casko1": self.insurance_casko1,
            "insurance_casko2": self.insurance_casko2,
            "insurance_casko3": self.insurance_casko3,
            "insurance_casko4": self.insurance_casko4,
            "insurance_casko5": self.insurance_casko5,
            "insurance_osago1": self.insurance_osago1,
            "insurance_osago2": self.insurance_osago2,
            "insurance_osago3": self.insurance_osago3,
            "insurance_osago4": self.insurance_osago4,
            "insurance_osago5": self.insurance_osago5,
            "health_insurance1": self.health_insurance1,
            "health_insurance1_str": self.health_insurance1_str,
            "health_insurance2": self.health_insurance2,
            "health_insurance2_str": self.health_insurance2_str,
            "health_insurance3": self.health_insurance3,
            "health_insurance3_str": self.health_insurance3_str,
            "health_insurance4": self.health_insurance4,
            "health_insurance4_str": self.health_insurance4_str,
            "health_insurance5": self.health_insurance5,
            "health_insurance5_str": self.health_insurance5_str,
            "other_insurance1": self.other_insurance1,
            "other_insurance1_str": self.other_insurance1_str,
            "other_insurance2": self.other_insurance2,
            "other_insurance2_str": self.other_insurance2_str,
            "other_insurance3": self.other_insurance3,
            "other_insurance3_str": self.other_insurance3_str,
            "other_insurance4": self.other_insurance4,
            "other_insurance4_str": self.other_insurance4_str,
            "other_insurance5": self.other_insurance5,
            "other_insurance5_str": self.other_insurance5_str,
        }


class LeasingItem(db.Model):
    """Модель для автоподсказок по имени предмета лизинга"""

    __tablename__ = "leas_items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)


class CalculateResultSchedule(db.Model):
    """Модель для хранения графиков расчета"""

    __tablename__ = "calculate_result_schedules"

    id = db.Column(db.Integer, primary_key=True)
    calc_id = db.Column(db.Integer, db.ForeignKey("leas_calculator.id"), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    leas_payment_amount = db.Column(db.Float, nullable=False)
    leas_payment_amount_str = db.Column(db.String(255), nullable=False)
    early_repayment_amount = db.Column(db.Float, nullable=False)
    early_repayment_amount_str = db.Column(db.String(255), nullable=False)

    # Обратное отношение к LeasCalculator
    leas_calculator = relationship("LeasCalculator", back_populates="payment_schedules")


class Seller(db.Model):
    """Модель для хранения информации о продавце"""

    __tablename__ = "sellers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    inn = db.Column(db.String(20), nullable=False, unique=True)
    ogrn = db.Column(db.String(20), nullable=False)
    okato = db.Column(db.String(20), nullable=True)
    kpp = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    signer = db.Column(db.String(255), nullable=True)
    based_on = db.Column(db.String(200), nullable=True)
    current_account = db.Column(db.String(30), nullable=True)
    date_of_registration = db.Column(db.Date, nullable=True)
    bank_id = db.Column(db.Integer, db.ForeignKey("banks.id"), nullable=True)

    leas_calculators = relationship("LeasCalculator", back_populates="seller")
    bank = relationship("Bank", back_populates="sellers")
