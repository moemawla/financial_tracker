from flask import Blueprint, request, render_template, redirect, url_for, abort
from sqlalchemy.sql.expression import desc
from models.countries import Country
from models.addresses import Address
from main import db, lm
from models.users import User
from schemas.user_schema import user_schema, user_update_schema
from flask_login import login_user, logout_user, login_required, current_user
from marshmallow import ValidationError

@lm.user_loader
def load_user(user):
    return User.query.get(user)

@lm.unauthorized_handler
def unauthorized():
    return redirect('/users/login/')

users = Blueprint('users', __name__)

@users.route('/users/signup/', methods = ['GET', 'POST'])
def sign_up():
    data = {'page_title': 'Sign Up'}
    
    if request.method == 'GET':
        return render_template('signup.html', page_data = data)
    
    new_user = user_schema.load(request.form)

    existing_user = User.query.filter_by(email = new_user.email).first()
    if existing_user:
        abort(409, 'An account with the provided email already exists')

    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect(url_for('transactions.get_transactions'))

@users.route('/users/login/', methods = ['GET', 'POST'])
def log_in():
    data = {'page_title': 'Log In'}

    if request.method == 'GET':
        return render_template('login.html', page_data = data)

    user = User.query.filter_by(email = request.form['email']).first()
    if user and user.check_password(password = request.form['password']):
        login_user(user)
        return redirect(url_for('transactions.get_transactions'))
    
    abort(401, 'Login unsuccessful. Did you supply the correct username and password?')

@users.route('/users/account/', methods = ['GET', 'POST'])
@login_required
def user_detail():
    if request.method == 'GET':
        data = {
            'page_title': 'Account Details',
            'countries' : Country.query.filter_by(active=True).order_by(Country.name).all()
        }

        address = Address.query.filter_by(resident_id=current_user.id).first()
        if address:
            data['address'] = address

        return render_template('user_detail.html', page_data = data)

    user = User.query.filter_by(id = current_user.id)
    updated_fields = user_schema.dump(request.form)
    errors = user_update_schema.validate(updated_fields)
    
    if errors:
        raise ValidationError(message = errors)

    existing_user = User.query.filter_by(email = updated_fields['email']).first()
    if existing_user and existing_user.id != current_user.id:
        abort(409, 'The provided email is used by a different account')

    user.update(updated_fields)
    db.session.commit()
    return redirect(f"{url_for('users.user_detail')}/")

@users.route('/users/logout/', methods = ['POST'])
@login_required
def log_out():
    logout_user()
    return redirect(url_for('users.log_in'))
