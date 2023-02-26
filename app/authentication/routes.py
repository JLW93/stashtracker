from forms import UserLoginForm, UserSignUpForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash # try to make flash work

from flask_login import login_user, logout_user, LoginManager, current_user, login_required

import time

auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserSignUpForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            confirm_email = form.confirm_email.data
            password = form.password.data
            confirm_password = form.confirm_password.data

            if email == confirm_email and password == confirm_password:
                user = User(email, password = password)

                db.session.add(user)
                db.session.commit()
            
                flash(f'You have successfully created a user account for {email}. Redirecting in 6 seconds...', 'User-created')

                time.sleep(6)

                return redirect(url_for('site.home'))

            else:
                flash('Username or Password does not match.')
    
    except:
        raise Exception('Invalid entry: Please try again.')

    return render_template('sign_up.html', form = form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('Login successful. Redirecting in 6 seconds...', 'auth-success')
                time.sleep(6)
                return redirect(url_for('site.home'))
            else:
                flash('Failed to log in. Please try again.', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid entry: Please try again.')
    return render_template('sign_in.html', form = form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))