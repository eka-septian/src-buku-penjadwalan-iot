from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from . import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    username = mapped_column(String(), unique=True, nullable=False)
    password_hashed = mapped_column(String(255), nullable=False)
    registered_on = mapped_column(DateTime(), nullable=False)

    def __init__(self, username: str, password_plaintext: str):
        self.username = username
        self.password_hashed = self._generate_password_hash(password_plaintext)
        self.registered_on = datetime.now()

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    def set_password(self, password_plaintext: str):
        self.password_hashed = self._generate_password_hash(password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def __repr__(self):
        return f"<User: {self.username}>"
