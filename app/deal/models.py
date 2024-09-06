from datetime import datetime

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

    leas_calculators = relationship("LeasCalculator", back_populates="deal")

    @classmethod
    def generate_dl_number(cls):
        current_year = str(datetime.now().year)[2:]
        start_number = 1

        while True:
            for_web = f"{start_number}/{current_year}"
            for_windows = f"{start_number}-{current_year}"
            existing_deal = cls.query.filter_by(dl_number=for_web).first()
            if not existing_deal:
                return for_web, for_windows
            start_number += 1

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
        }

    def can_add_leas_calculator(self):
        """
        Проверяет, можно ли добавить еще один LeasCalculator к этой сделке.
        """
        return len(self.leas_calculators) < self.deals_count
