from flask import Blueprint, render_template, request, url_for, flash, redirect
from .models import User, Borrower
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .token import generate_confirmation_token, confirm_token
from datetime import datetime
from .email import send_email

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'POST':
    email_user = request.form.get('email_user')
    password = request.form.get('password')

    user = User.query.filter_by(email=email_user).first()
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
      user = User.query.filter_by(username=email_user).first()
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
        flash('User does not exist! Please check for any typos!', category='error')

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

    user_email = User.query.filter_by(email=email).first()
    name = User.query.filter_by(username=username).first()

    if name:
      flash('Username already taken!', category='error')
    else:
      if len(username) < 3:
        flash('Username must be more than 3 characters!', category='error')
      elif len(username) > 15:
        flash('Username exceeds character limit!', category='error')
      elif user_email:
        flash('Email already exists.', category='error')
      elif len(email) < 4:
        flash('Email must be more than 3 characters!', category='error')
      elif password1 != password2:
        flash('Passwords do not match!', category='error')
      elif len(password1) < 7:
        flash('Password must be greater than 7 characters!', category='error')
      else:
        new_user = User(username=username, email=email, password=generate_password_hash(password1, method='sha256'), admin=False, confirmed=False)

        db.session.add(new_user)
        db.session.commit()


        token = generate_confirmation_token(email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('user/activate.html', confirm_url=confirm_url)

        subject = "Please confirm your email"
        send_email(email, subject, html)

        login_user(new_user, remember=True)

        flash('A confirmation email has been sent via email.', category='success')
        return redirect(url_for('views.home', token=token))

  return render_template("sign_up.html", user=current_user)

@auth.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', category='danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', category='success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!',  category='success')
    return redirect(url_for('views.home', user=current_user))

@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('views.home', user=current_user))
    flash('Please confirm your account!', category='warning')
    return render_template('unconfirmed.html', user=current_user)