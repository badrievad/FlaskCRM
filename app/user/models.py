from uuid import uuid4

from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(length=50), unique=True)
    password = db.Column(db.String(length=200))
    blocked = db.Column(db.Boolean())
    role = db.Column(db.String(length=50))
    fullname = db.Column(db.String())
    abbreviation_name = db.Column(db.String())
    email = db.Column(db.String(length=50))
    url_photo = db.Column(db.String())
    worknumber = db.Column(db.String())
    mobilenumber = db.Column(db.String())
    fon_url = db.Column(db.String(), default="images/background/default.jpg")
    telegram = db.Column(db.String(length=50))

    # Поле для хранения идентификатора активной сессии
    active_session_id = db.Column(db.String(36), nullable=True)

    deals = relationship("Deal", back_populates="user")  # Связь с моделью Deal

    def set_active_session(self):
        """Устанавливаем новый идентификатор активной сессии."""
        self.active_session_id = str(uuid4())
        db.session.commit()

    def clear_active_session(self):
        """Очищаем идентификатор активной сессии при выходе."""
        self.active_session_id = None
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_manager(self):
        return self.role == "manager"

    @property
    def is_risk(self):
        return self.role == "risk"

    @property
    def is_tester(self):
        return self.role == "tester"

    @property
    def is_blocked(self):
        return self.blocked is True

    def __repr__(self):
        return f"Пользователь: {self.login}"

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def get_name(self):
        return self.fullname if self.fullname else self.login
