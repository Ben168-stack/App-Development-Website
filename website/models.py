from datetime import datetime,timedelta
from website import db, login_manager
from website import
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False, unique=True)
    budget = db.Column(db.Integer(), nullable=False, default=10000)
    # items = db.relationship('Item', backref='owned_user', lazy=True)
    @property
    def prettier_budget(self):
        # to confirm this is to add a , in the budget
        # e.g 1,000 or 100,000
        # this relies on logic alone not special class names
        # affecting this function
        if len(str(self.budget)) >= 4:
            return f'${str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return f"${self.budget}"