from .models import Group
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, current_user
from .models import Group, Payment, Member
from . import db
import uuid
from datetime import datetime
from dateutil import parser
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def create_payment():
    group = Group.query.filter_by(name="test").first()
    login_user(group, remember=True)

    if request.method == 'POST':
        # Retrieve data from form
        name = request.form.get('name')
        amount = request.form.get('amount')
        currency = request.form.get('currency')
        payer = request.form.get('payer')
        debtors = request.form.get('debtors')
        date_str = request.form.get('date')
        note = request.form.get('note')
        tDate = datetime.now()

        # Perform input validation
        if not isinstance(name, str):
            flash('Name must be strings.',  category='error')
            return render_template("home.html", group=current_user)

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except (ValueError, TypeError):
            flash("Please enter amount", category='error')
            return render_template("home.html", group=current_user)

        if len(currency) != 3 or not currency.isalpha():
            flash('Currency must be a 3-letter code.', category='error')
            return render_template("home.html", group=current_user)

        if not isinstance(payer, str) or not isinstance(debtors, str) or len(payer) == 0 or len(debtors) == 0:
            flash(f'{payer} {debtors}Payer and debtors must be strings.',
                  category='error')
            return render_template("home.html", group=current_user)

        try:
            date = parser.parse(date_str)
        except ValueError:
            if date_str == '':
                date = datetime(tDate.year, tDate.month,
                                tDate.day, tDate.hour, tDate.minute)
            else:
                flash("Date has a incorrect format",
                      category='error')
                return render_template("home.html", group=current_user)

        if note is not None and not isinstance(note, str):
            flash('Note must be a string or blank.', category='error')
            return render_template("home.html", group=current_user)

        payment = Payment(name=name, amount=amount, currency=currency, payer=payer,
                          debtors=debtors, date=date, note=note, group_id=current_user.id)
        db.session.add(payment)

        db.session.commit()

    return render_template("home.html", group=current_user)


@views.route('/debts', methods=['GET', 'POST'])
def settle_debt():
    return render_template("debts.html", group=current_user)


@views.route('/delete-payment', methods=['POST'])
def delete_payment():
    payment = json.loads(request.data)
    paymentId = payment['paymentId']
    payment = Payment.query.get(paymentId)
    if payment:
        if payment.group_id == current_user.id:
            db.session.delete(payment)
            db.session.commit()

    return jsonify({})
