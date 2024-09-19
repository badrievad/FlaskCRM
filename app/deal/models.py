from datetime import datetime

from sqlalchemy import Sequence
from sqlalchemy.orm import relationship

from .. import db


class Deal(db.Model):
    __tablename__ = "deals"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    name_without_special_symbols = db.Column(db.String(200), nullable=False)
    company_inn = db.Column(db.String(20), nullable=False)
    created_by = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    archived_at = db.Column(db.DateTime, nullable=True)
    dl_number = db.Column(db.String(20), nullable=True, default="б/н")
    dl_number_windows = db.Column(db.String(20), nullable=True, default="б-н")
    product = db.Column(
        db.String(50), nullable=False, default="Статус продукта еще не определен"
    )
    deals_count = db.Column(db.Integer, default=1)
    deal_path = db.Column(db.String(500), nullable=True)
    group_id = db.Column(db.String(50), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))

    sequence_number = db.Column(db.Integer, nullable=False)
    year = db.Column(db.String(2), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("sequence_number", "year", name="uq_sequence_year"),
    )

    leas_calculators = relationship("LeasCalculator", back_populates="deal")
    client = relationship("Client", back_populates="deals")

    @classmethod
    def generate_dl_number(cls):
        current_year = datetime.now().strftime("%y")  # Последние две цифры года

        # Получаем следующее значение из последовательности
        sequence = Sequence("deal_sequence")
        sequence_value = db.session.execute(sequence)

        dl_number = f"{sequence_value}/{current_year}"
        dl_number_windows = f"{sequence_value}-{current_year}"

        return sequence_value, current_year, dl_number, dl_number_windows

    def to_json(self) -> dict:
        """При добавлении или удалении столбца в модели всегда корректируем эту функцию!"""
        if self.archived_at is None:
            archived_at = None
        else:
            archived_at = self.archived_at.strftime("%d.%m.%Y %H:%M:%S")
        return {
            "id": self.id,
            "product": self.product,
            "title": self.title,
            "company_inn": self.company_inn,
            "created_by": self.created_by,
            "created_at": self.created_at.strftime("%d.%m.%Y %H:%M:%S"),
            "archived_at": archived_at,
            "dl_number": self.dl_number,
            "dl_number_windows": self.dl_number_windows,
            "sequence_number": self.sequence_number,
            "year": self.year,
        }

    def can_add_leas_calculator(self):
        """
        Проверяет, можно ли добавить еще один LeasCalculator к этой сделке.
        """
        return len(self.leas_calculators) < self.deals_count


class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    inn = db.Column(db.String(20), nullable=False, unique=True)
    ogrn = db.Column(db.String(20), nullable=False)
    okato = db.Column(db.String(20), nullable=True)
    kpp = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    signer = db.Column(db.String(100), nullable=True)
    based_on = db.Column(db.String(200), nullable=True)
    current_account = db.Column(db.String(30), nullable=True)
    date_of_registration = db.Column(db.Date, nullable=True)
    bank_id = db.Column(db.Integer, db.ForeignKey("banks.id"), nullable=True)

    deals = relationship("Deal", back_populates="client")
    bank = relationship("Bank", back_populates="clients")


class Bank(db.Model):
    __tablename__ = "banks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    inn = db.Column(db.String(20), nullable=False, unique=True)
    kpp = db.Column(db.String(20), nullable=False)
    bic = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    correspondent_account = db.Column(db.String(20), nullable=True)

    clients = relationship("Client", back_populates="bank")
    sellers = relationship("Seller", back_populates="bank")
