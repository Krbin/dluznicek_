
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    payer = db.Column(db.String(50), nullable=False)
    debtors = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    note = db.Column(db.String(255), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))


class Group(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    payments = db.relationship('Payment')


class Debtor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    debts = db.Column(db.ARRAY(String))
