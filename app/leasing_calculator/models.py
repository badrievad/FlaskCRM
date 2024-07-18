from .. import db


class LeasCalculator(db.Model):
    __tablename__ = "leas_calculator"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    manager_login = db.Column(db.String(200), nullable=False)
    deal_id = db.Column(db.Integer, db.ForeignKey("deals.id"), nullable=True)
    date = db.Column(db.Date, nullable=False)
    date_ru = db.Column(db.String(50), nullable=True)
    path_to_file = db.Column(db.String(500), nullable=True)
    item_name = db.Column(db.String(500), nullable=True)
    item_type = db.Column(db.String(150), nullable=True)
    item_price = db.Column(db.Numeric(precision=10, scale=2), nullable=True)
    item_price_str = db.Column(db.String(50), nullable=True)
    prepaid_expense = db.Column(db.Numeric(precision=10, scale=2), nullable=True)
    term = db.Column(db.Integer, nullable=True)
    interest_rate = db.Column(db.Float, nullable=True)


class LeasingItem(db.Model):
    __tablename__ = "leas_items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
