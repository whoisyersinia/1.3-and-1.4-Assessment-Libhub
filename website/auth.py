from flask import Blueprint, render_template, request, url_for, flash, redirect

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
  return render_template("login.html", boolean=True)

@auth.route('/logout')
def logout():
  return "<p>logout</p>"

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
  if request.method == 'POST':
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if len(email) < 4:
      flash('Email must be more than 3 characters!', category='error')
    elif password1 != password2:
      flash('Passwords do not match!', category='error')
    elif len(password1) < 7:
      flash('Password must be greater than 7 characters!', category='error')
    else:
      flash('Welcome to Libhub!', category='success')
      return redirect(url_for('views.home'))


  return render_template("sign_up.html")

