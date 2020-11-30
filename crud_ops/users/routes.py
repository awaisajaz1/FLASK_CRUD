from flask import render_template, url_for, redirect, flash, request, abort, Blueprint
from crud_ops.users.forms import LoginForm, RegistrationForm, updateForm
from crud_ops.models import Post, User
from crud_ops import  db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, timedelta


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, image_file='sample', password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return e
        flash('Account has been created, You can log in now!', 'success')
        redirect(url_for('main.home'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        userExists = User.query.filter_by(email=form.email.data).first()
        if userExists and bcrypt.check_password_hash(userExists.password, form.password.data):
            login_user(userExists, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check credentials', 'danger')
    return render_template('logins.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))



@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = updateForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        try:
            db.session.commit()
        except:
            return 'Update Form has issue'
        redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)