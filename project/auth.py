from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
import jsonify
from . import db
# https://prod.liveshare.vsengsaas.visualstudio.com/join?7174E3856CBFA5BD076070B8632B16F383B0

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    data = request.json
    print("req ", data["username"])
    username = data["username"]
    password = data["password"]

    # user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    user = User.query.filter_by(username=username).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Username already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    # new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/login', methods=['POST'])
def login_post():
    data = jsonify(request.json)

    # login code goes here
    username = data["username"]
    password = data["password"]
    print("passwordddddddd: ", password)

    remember = True if request.form.get('remember') else False

    # user = User.query.filter_by(email=email).first()
    user = User.query.filter_by(username=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        return None

    return user
    
    # if not user or not check_password_hash(user.password, password):
    #     flash('Please check your login details and try again.')
    #     print(user.username)
    #     print(check_password_hash(user.password, password))
    #     return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    # login_user(user, remember=remember)
    # return redirect(url_for('main.profile'))