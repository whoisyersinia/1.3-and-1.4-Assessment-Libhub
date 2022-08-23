from flask import Blueprint, render_template, request, url_for, flash, redirect
from .models import User, Borrower
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
      if check_password_hash(user.password, password):
        flash('Logged in sucessfully!', category='success')
        if request.form.get('remember_me'):
          login_user(user, remember=True)
        else:
          login_user(user)
        return redirect(url_for('views.home'))
      else:
        flash('Incorrect password, please try again!', category='error')
    else: 
      flash('Email does not exist!', category='error')

  return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
  if request.method == 'POST':
    username = request.form.get('username')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    user = User.query.filter_by(email=email).first()
    name = User.query.filter_by(username=username).first()
    if name:
      flash('Username already taken.', category='error')
    else:
      if user:
        flash('Email already exists.', category='error')
      elif len(email) < 4:
        flash('Email must be more than 3 characters!', category='error')
      elif password1 != password2:
        flash('Passwords do not match!', category='error')
      elif len(password1) < 7:
        flash('Password must be greater than 7 characters!', category='error')
      else:
        new_user = User(username=username, email=email, password=generate_password_hash(password1, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user, remember=True)

        flash('Welcome to Libhub!', category='success')
        return redirect(url_for('views.home'))

  return render_template("sign_up.html", user=current_user)

