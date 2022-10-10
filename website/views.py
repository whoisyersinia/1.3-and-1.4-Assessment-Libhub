from flask import Blueprint, render_template, request, url_for, flash, redirect, abort
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import db
from .models import User, Borrowed_book, Book, Borrower, Lender


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
  if request.method == 'POST':
    term = request.form.get('search')
    
    return redirect(url_for('views.search', searchterm=term))

  return render_template("index.html", user=current_user)

@views.route('/termsandconditions')
def tandc():
  return render_template('tc.html')

@views.route('/privacypolicy')
def privacy():
  return render_template('privacypolicy.html')

@views.route('/books')
def books():
  if current_user.is_authenticated is True :
    books = Book.query.filter(Book.lender_id != current_user.id).order_by(Book.created_on).limit(4).all()
  else:
    books = Book.query.order_by(Book.created_on).limit(4).all()
  return render_template("books.html", user=current_user, books=books)

@views.route('/search/<path:searchterm>')
def search(searchterm):
  term = "%{}%".format(searchterm)

  search = Book.query.filter((Book.title.like(term)) | (Book.author.like(term)) | Book.lender_username.like(term)).all()
  
  return render_template('search.html', user=current_user, results=search, searchterm=searchterm)


@views.route('/user/<int:userid>')
def user(userid):

  user = User.query.get_or_404(userid)

  return render_template('user.html', userdetails=user, user=current_user)


@views.route('/dashboard/<int:user_id>', methods=['GET', 'POST'])
@login_required
def dashboard(user_id):

  if current_user.id != user_id:
    abort(403)

  user = User.query.filter_by(id=user_id).first()

  return render_template("dashboard/dashboard.html", user=user)

@views.route('/dashboard/booksborrowed/<int:user_id>')
@login_required
def borrowed(user_id):

  if current_user.id != user_id:
    abort(403)
  
  booksborrowed = Borrowed_book.query.get_or_404(user_id)
  books = Book.query.filter_by(id = booksborrowed.book_id)

  return render_template("dashboard/booksborrowed.html", user=current_user, books=books, booksborrowed=booksborrowed)

@views.route('/dashboard/bookslended/<int:user_id>')
@login_required
def lended(user_id):

  if current_user.id != user_id:
    abort(403)

  books = Book.query.filter_by(lender_id=user_id).all()

  return render_template("dashboard/bookslended.html", user=current_user, books=books)

@views.route('/dashboard/bookslended/bookstatus/<int:book_id>')
@login_required
def status(book_id):

  book = Book.query.get_or_404(book_id)

  borrowerlist = db.session.query(Borrower, Borrowed_book)\
    .filter(book_id == Borrowed_book.book_id)\
    .outerjoin(Borrowed_book, Borrowed_book.borrower_id==Borrower.id)\
    .add_columns(Borrower.username, Borrower.id, Borrowed_book.borrower_id)\
    .filter(Borrower.id == Borrowed_book.borrower_id).all()

 
  if current_user.id != book.lender_id:
    abort(403)


  return render_template("dashboard/bookstatus.html", user=current_user, books=book, borrowerlist=borrowerlist)

@views.route('/accept/<int:book_id>/borrower/<int:borrower_id>', methods=['GET', 'POST'])
@login_required
def accept(book_id, borrower_id):
  book = Book.query.get_or_404(book_id)
  requests = Borrowed_book.query.get(book_id)

  borrowerlist = db.session.query(Borrower, Borrowed_book)\
    .filter(book_id == Borrowed_book.book_id)\
    .filter(borrower_id == Borrowed_book.borrower_id)\
    .outerjoin(Borrower, Borrower.id==Borrowed_book.borrower_id)\
    .add_columns(Borrower.username, Borrower.id, Borrowed_book.borrower_id, Borrower.fName, Borrower.lName, Borrower.address1, Borrower.city, Borrower.phone)\
    .filter(Borrower.id == Borrowed_book.borrower_id).first()

  if current_user.id != book.lender_id:
    abort(403)

  else:
    if request.method == 'POST':

      accept = request.form.get('tcs')

      if not accept:
        flash('Please read and accept our terms and conditions!', category='error')
      else:
        requests.lender_confirm = True
        date_str = datetime.utcnow
        date_str = str(date_str)
        b = ".0"
        date_str = date_str + b
        date_object = datetime.strptime(date_str, '%y/%m/%d %H:%M:%S.%f')
        datenow = date_object.strftime('%m/%d/%y')
        requests.borrowed_date = datenow
        # requests.due_date =

        db.session.add(requests)
        db.session.commit()

        flash('Successfully confirmed! Now returning to dashboard', category='success')
        return redirect(url_for('views.dashboard', user_id=current_user.id))


  return render_template("accept.html", user=current_user, book=book, borrowerlist=borrowerlist)

# @views.route('/dashboard/bookslended/bookstatus/<int:book_id>', methods=['GET', 'POST'])
# @login_required
# def deny(book_id):

#   book = Book.query.get_or_404(book_id)

#   borrowerlist = db.session.query(Borrower, Borrowed_book)\
#     .filter(book_id == Borrowed_book.book_id)\
#     .outerjoin(Borrowed_book, Borrowed_book.borrower_id==Borrower.id)\
#     .add_columns(Borrower.username, Borrower.id, Borrowed_book.borrower_id)\
#     .filter(Borrower.id == Borrowed_book.borrower_id).all()

 
#   if current_user.id != book.lender_id:
#     abort(403)

 # return render_template("dashboard/bookstatus.html", user=current_user, books=book, details=details)


@views.route('/account/<int:user_id>', methods=['GET', 'POST'])
@login_required
def account(user_id):

  user = User.query.filter_by(id=user_id).first()

  if current_user.id != user_id:
    abort(403)

  else: 
    if request.method == 'POST':
      username = request.form.get('username')
      email = request.form.get('email')
    
      useremail = User.query.filter_by(email=email).first()
      name = User.query.filter_by(username=username).first()

      if name:
          if useremail:
           flash('Email already exists or email is identical to current email!', category='error')

          elif len(email) < 4:
            flash('Email must be more than 3 characters!', category='error')

          else:
            user.email = email
            db.session.add(user)
            db.session.commit()

            flash('Login details changed sucessfully. Please login again!', category='success')
            logout_user()
            return redirect(url_for('auth.login'))
      else:
        if name:
          flash('Username already taken or username is identical to current username!', category='error')
        else:
          if len(username) < 3:
            flash('Username must be more than 3 characters!', category='error')
          elif len(username) > 15:
            flash('Username exceeds character limit!', category='error')
          else:
            user.username = username
            db.session.add(user)
            db.session.commit()

            flash('Login details changed sucessfully. Please login again!', category='success')
            logout_user()
            return redirect(url_for('auth.login'))

  return render_template("dashboard/account.html", user=current_user)


@views.route('/account/passwordreset/<int:user_id>', methods=['GET', 'POST'])
@login_required
def passreset(user_id):
  user = User.query.filter_by(id=user_id).first()

  if current_user.id != user_id:
    abort(403)

  else: 
    if request.method == 'POST':
      currentpassword = request.form.get('currentpassword')
      newpassword = request.form.get('newpassword')
      confirmpassword = request.form.get('confirmpassword')

      userpass = User.query.filter_by(id=user_id).first()

   
      if check_password_hash(userpass.password, currentpassword):
        if newpassword == currentpassword:
          flash('Please create a new password!', category='error')
        elif len(newpassword) < 7:
          flash('Password must be greater than 7 characters!', category='error')
        elif confirmpassword != newpassword:
          flash('Passwords do not match!', category='error')

        else:
          user.password = generate_password_hash(newpassword, method='sha256')

          db.session.add(user)
          db.session.commit()

          flash('Password changed sucessfully', category='success')
          logout_user()
          return redirect(url_for('auth.login'))
      else:
         flash('Password does not match. Please try again!', category='error')

  return render_template("dashboard/passreset.html", user=current_user)

@views.route('/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit(book_id):

  book = Book.query.get_or_404(book_id)

  if current_user.id != book.lender_id:
    abort(403)
    
  else:
    if request.method == 'POST':
      title = request.form.get('title')
      author = request.form.get('author')
      delete = request.form.get('delete')
      
      if len(delete) == 0:
        if len(title) > 150:
          flash('Title exceeds character limit!', category='error')
        elif len(title) < 2:
          flash('Title must be greater than 2 characters!', category='error')
        elif len(author) < 3:
          flash('Author must be greater than 3 characters!', category='error')
        elif len(author) > 256:
          flash('Author exceeds character limit!', category='error')
        elif title == book.title and author == book.author:
          flash('Please edit to continue!', category='error')

        else:
          book.title = title
          book.author = author

          db.session.add(book)
          db.session.commit()

          flash('Book sucessfully edited', category='success')
          return redirect(url_for('views.books'))

      else:
        if delete != title:
          flash('Please try again to confirm for deletion!', category='error')
        else:
          db.session.delete(book)
          db.session.commit()

          flash('Book sucessfully deleted!', category='success')
          return redirect(url_for('views.books'))

  return render_template("edit.html", user=current_user, book=book)
   

@views.route('/lend', methods=['GET', 'POST'])
@login_required
def lend():
  if request.method == 'POST':
    
    book = Book.query.filter_by(lender_id=current_user.id).all()

    accept = request.form.get('tcs')
    title = request.form.get('title')
    author = request.form.get('author')

    if len(title) > 150:
      flash('Title exceeds character limit!', category='error')
    elif len(title) < 2:
      flash('Title must be greater than 2 characters!', category='error')
    elif len(author) < 3:
      flash('Author must be greater than 3 characters!', category='error')
    elif len(author) > 256:
      flash('Author exceeds character limit!', category='error')
    elif not accept:
      flash('Please read and accept our terms and conditions!', category='error')
    else:
      book = Book(title=title, author=author, lender_id=current_user.id, lender_username=current_user.username)
      db.session.add(book)
      db.session.commit()

      flash('Book sucessfully added', category='success')
      return redirect(url_for('views.books'))

  return render_template("lend.html", user=current_user)

@views.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
@login_required
def borrow(book_id):

  books = Book.query.get_or_404(book_id)

  if current_user.id == books.lender_id:
    abort(403)

  if request.method == 'POST':
    fName = request.form.get('fName')
    lName = request.form.get('lName')
    address1 = request.form.get('address')
    city = request.form.get('city')
    phone = request.form.get('phone')
    accept = request.form.get('tcs')

    phone_check = Borrower.query.filter_by(phone=phone).first()
    id = Borrower.query.filter_by(user_id=current_user.id).first()
    if phone_check:
      flash('Phone number already in use!', category='error')
    elif id:
      flash('Request already sent!', category='error')
      return redirect(url_for('views.books'))
    else:
      if len(fName) > 150:
        flash('First name exceeds character limit!', category='error')
      elif len(fName) < 1:
        flash('First name must be more than one character!', category='error')
      elif len(lName) > 150:
        flash('Last name exceeds character limit!', category='error')
      elif len(lName) < 1:
        flash('Last name must be more than one character!', category='error')
      elif len(address1) > 150:
        flash('Address exceeds character limit!', category='error')
      elif len(address1) < 8:
        flash('Address must be more than eight characters!', category='error')
      elif len(city) > 80:
        flash('City exceeds character limit!', category='error')
      elif len('City') < 2:
        flash('City must be more than two characters!', category='error')
      elif len(phone) > 10:
        flash('Phone exceeds character limit!', category='error')
      elif len(lName) < 8:
        flash('Phone must be more than eight characters!', category='error')
      elif not accept:
        flash('Please read and accept our terms and conditions!', category='error')
      else:
        if not id:
          borrower = Borrower(fName=fName, lName=lName, address1=address1, city=city, username=current_user.username, email=current_user.email, phone=phone, user_id=current_user.id)
          requests = Borrowed_book(return_book=False, lender_confirm=False, borrower_id=current_user.id, book_id=book_id)
          db.session.add(borrower)

        else:
          requests = Borrowed_book(return_book=False, lender_confirm=False, borrower_id=current_user.id, book_id=book_id)

        db.session.add(requests)
        db.session.commit()
        
        flash('Lender notifed, please wait for response!', category='success')
        return redirect(url_for('views.books'))


  return render_template("borrow.html", user=current_user, book=books)
  