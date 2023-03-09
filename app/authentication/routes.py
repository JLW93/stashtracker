from forms import UserLoginForm, UserSignUpForm
from models import User, db, check_password_hash, generate_password_hash, user_schema
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify # try to make flash work
from helpers import token_required

from flask_login import login_user, logout_user, LoginManager, current_user, login_required

import time

auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserSignUpForm()

    try:
        if request.method == 'POST':
            # email = form.email.data
            # confirm_email = form.confirm_email.data
            # password = form.password.data
            # confirm_password = form.confirm_password.data
            data = request.get_json()
            email = data['email']
            confirm_email = data['confirmEmail']
            password = data['password']
            confirm_password = data['confirmPassword']

            if email == confirm_email and password == confirm_password:
                user = User(email, password = password)

                db.session.add(user)
                db.session.commit()
            
                flash(f'You have successfully created a user account for {email}. Redirecting in 3 seconds...', 'User-created')

                time.sleep(3)

                # return redirect(url_for('site.home'))
                return jsonify({'message': 'Account created successfully!'}), 201

            else:
                # flash('Username or Password does not match.')
                return jsonify({'error': 'Email or Password do not match.'}), 400
    
    except:
        raise Exception('Invalid entry: Please try again.')

    return render_template('sign_up.html', form = form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    print(request.data)
    print(request.get_json())

    data = request.get_json()
    email = data['email']
    password = data['password']
    try:
        if request.method == 'POST':
            # email = form.email.data
            # password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                token = logged_user.token

                return jsonify({"token": token})
                
            else:
                
                return jsonify({"error": "Invalid Email or Password."}), 401
    except:
        raise Exception('Invalid entry: Please try again.')
    return 'test'

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))

# change first name and last name
@auth.route('/update-data', methods = ['PUT'])
@token_required
def update_user_data(current_user_token):
    data = request.get_json()
    token = current_user_token.token

    user = User.query.filter(User.token == token).first()

    if not user:
        return 'User not found or incorrect token', 404
    
    if not token:
        return 'Token not found', 404
    
    try:
        user.first_name = request.json.get('first_name', user.first_name)
        user.last_name = request.json.get('last_name', user.last_name)
        db.session.commit()
    except:
        raise Exception('Missing required data.')

# change password
@auth.route('/update-password', methods = ['PUT'])
@token_required
def update_password(current_user_token):
    data = request.get_json()
    token = current_user_token.token
    old_password = data['old_password']
    new_password = data['new_password']

    user = User.query.filter(User.token == token).first()

    if not user:
        return 'User not found', 404
    
    if not token:
        return 'Invalid token or token not found', 404
    
    if not old_password or not new_password:
        return 'Incorrect or missing password.', 404
    
    if user and check_password_hash(user.password, old_password):
        new_pw_hash = generate_password_hash(new_password)
        user.password = new_pw_hash

        db.session.commit()

        return jsonify({'message': 'Password Updated!'}), 201
    return 'test'


# get data to display on front end
@auth.route('/get-user-data', methods = ['GET'])
@token_required
def get_user_data(current_user_token):
    token = current_user_token.token

    user = User.query.filter(User.token == token).first()

    if not user:
        return 'User not found', 404

    response = user_schema.dump(user)
    return jsonify(response)