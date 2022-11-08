from flask import Blueprint, render_template, request, url_for, flash, redirect, abort
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from . import db
from .models import User, Borrowed_book, Book, Borrower, Lender


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
  """'
  This is my home page, users can search books here
  """
  if request.method == 'POST':
    term = request.form.get('search')
    
    return redirect(url_for('views.search', searchterm=term))

  return render_template("index.html", user=current_user)

@views.route('/termsandconditions')
def tandc():
  """
  This is my terms and conditions page
  """
  return render_template('tc.html')

@views.route('/privacypolicy')
def privacy():
  """
  This is my privacy policy page
  """
  return render_template('privacypolicy.html')

@views.route('/books')
def books():
  """
  This is my books page, it prints out the first 4 recently added books that current user does not own.
  """
  if current_user.is_authenticated is True:
    books = Book.query.filter(Book.lender_user_id != current_user.id)\
    .order_by(Book.created_on.desc()).limit(4).all()
  else:
    books = Book.query.order_by(Book.created_on).limit(4).all()
  return render_template("books.html", user=current_user, books=books)

@views.route('/search/<path:searchterm>')
def search(searchterm):
  """
  This is my search page, users redirect to this page once they've searched in the home page.
  """
  
  term = "%{}%".format(searchterm)

  search = Book.query.filter((Book.title.like(term)) | (Book.author.like(term)) | (Book.lender_username.like(term))).all()
  
  return render_template('search.html', user=current_user, results=search, searchterm=searchterm)


@views.route('/user/<int:userid>')
def user(userid):
  """
  This prints user information
  """

  user = User.query.get_or_404(userid)

  return render_template('user.html', userdetails=user, user=current_user)


@views.route('/dashboard/<int:user_id>', methods=['GET', 'POST'])
@login_required
def dashboard(user_id):
  """
  This is the base dashboard page, users must be logged in to access
  """

  if current_user.id != user_id:
    abort(403)

  user = User.query.filter_by(id=user_id).first()

  return render_template("dashboard/dashboard.html", user=user)

@views.route('/dashboard/booksborrowed/<int:user_id>')
@login_required
def borrowed(user_id):
  """
  This is borrowed page, it takes the current user id and checks if they have books borrowed under their account and prints it out on the page.
  """
  if current_user.id != user_id:
    abort(403)

  borrower = Borrower.query.filter_by(user_id=user_id).first()

  if not borrower:
    flash('Enter personal details!', category='error')
    return redirect(url_for('views.infoedit', user_id=current_user.id))
  else:
    bookslist = db.session.query(Borrowed_book, Book)\
      .filter(Borrowed_book.borrower_id == borrower.id)\
      .filter(Borrowed_book.return_confirm == False)\
      .outerjoin(Borrowed_book, Borrowed_book.book_id == Book.id)\
      .add_columns(Book.id, Book.lender_user_id, Borrowed_book.due_date, Borrowed_book.return_book, Borrowed_book.return_confirm, Book.title, Book.author, Book.lender_username, Borrowed_book.lender_confirm, Borrowed_book.lender_id)\
      .filter(Book.id == Borrowed_book.book_id).all()

  datenow = datetime.today()

  return render_template("dashboard/booksborrowed.html", user=current_user, bookslist=bookslist, datenow=datenow)

@views.route('/dashboard/bookslended/<int:user_id>')
@login_required
def lended(user_id):
  """
  This is my lended page, it takes the current user id and checks if they have books that they've lended on the system and it prints it out on the page. 
  """

  if current_user.id != user_id:
    abort(403)

  books = Book.query.filter_by(lender_user_id=user_id).all()

  return render_template("dashboard/bookslended.html", user=current_user, books=books)

@views.route('/dashboard/bookslended/bookstatus/<int:book_id>')
@login_required
def status(book_id):
  """
  This is my status page, it takes the book id that the user has lended and checks if anyone has requested or is currently borrowing that book. 
  """

  book = Book.query.get_or_404(book_id)


  borrowerlist = db.session.query(Borrower, Borrowed_book)\
    .filter(book_id == Borrowed_book.book_id)\
    .filter(Borrowed_book.return_confirm == False)\
    .outerjoin(Borrowed_book, Borrowed_book.borrower_id==Borrower.id)\
    .add_columns(Borrower.username, Borrower.id, Borrowed_book.borrower_id, Borrowed_book.lender_confirm, Borrowed_book.return_book)\
    .filter(Borrower.id == Borrowed_book.borrower_id)\
    .order_by(Borrowed_book.borrowed_date).all()
  
  if current_user.id != book.lender_user_id:
    abort(403)

  return render_template("dashboard/bookstatus.html", user=current_user, books=book, borrowerlist=borrowerlist)

@views.route('/deny/<int:book_id>/borrower/<int:borrower_id>', methods=['GET', 'POST'])
@login_required
def deny(book_id, borrower_id):
  """
  This allows the lender to deny a user to borrow a book.
  """
  book = Book.query.get_or_404(book_id)

  requests = Borrowed_book.query.filter_by(borrower_id=borrower_id).filter_by(book_id=book_id).filter_by(return_confirm = False).first()

  borrowerlist = db.session.query(Borrower, Borrowed_book)\
    .filter(book_id == Borrowed_book.book_id)\
    .filter(borrower_id == Borrowed_book.borrower_id)\
    .outerjoin(Borrower, Borrower.id==Borrowed_book.borrower_id)\
    .add_columns(Borrower.username, Borrower.id, Borrowed_book.borrower_id, Borrower.fName, Borrower.lName, Borrower.address1, Borrower.city, Borrower.phone, Borrowed_book.lender_confirm)\
    .filter(Borrower.id == Borrowed_book.borrower_id).first()

  if current_user.id != book.lender_user_id:
    abort(403)


  else:
    if request.method == 'POST':
      for borrower in borrowerlist:
        borrower = Borrowed_book.query.filter_by(borrower_id=borrower_id).filter_by(book_id=book_id).filter_by(return_confirm = False).first()

      accept = request.form.get('tcs')

      if borrower.lender_confirm:
        flash('Book already being borrowed.', category='error')
        return redirect(url_for('views.status', book_id=book_id))    

      elif not accept:
        flash('Please read and accept our terms and conditions!', category='error')

      else:
        db.session.delete(requests)
        db.session.commit()

        flash('Successfully deleted! Now returning to dashboard', category='success')
        return redirect(url_for('views.status', book_id=book_id))    

  return render_template("deny.html", user=current_user, book=book, borrowerlist=borrowerlist)



@views.route('/accept/<int:book_id>/borrower/<int:borrower_id>', methods=['GET', 'POST'])
@login_required
def accept(book_id, borrower_id):
  """
  This allows the lender to accept requests, it sets the due date to weeks from hitting the accept button on this page. 
  """
  book = Book.query.get_or_404(book_id)

  requests = Borrowed_book.query.filter_by(borrower_id=borrower_id).filter_by(book_id=book_id).filter_by(return_confirm = False).first()

  borrowerlist = db.session.query(Borrower, Borrowed_book)\
    .filter(book_id == Borrowed_book.book_id)\
    .filter(borrower_id == Borrowed_book.borrower_id)\
    .outerjoin(Borrower, Borrower.id==Borrowed_book.borrower_id)\
    .add_columns(Borrower.username, Borrower.id, Borrowed_book.borrower_id, Borrower.fName, Borrower.lName, Borrower.address1, Borrower.city, Borrower.phone, Borrowed_book.lender_confirm)\
    .filter(Borrower.id == Borrowed_book.borrower_id).first()

  borrower_exists = db.session.query(Borrower, Borrowed_book)\
    .filter(borrower_id == Borrowed_book.borrower_id)\
    .filter(Borrowed_book.lender_confirm == True)\
    .outerjoin(Borrower, Borrower.id==Borrowed_book.borrower_id)\
    .filter(Borrower.id == Borrowed_book.borrower_id).first()

  if current_user.id != book.lender_user_id:
    abort(403)


  else:
    if request.method == 'POST':
      for borrower in borrowerlist:
        borrower = Borrowed_book.query.filter_by(borrower_id=borrower_id).filter_by(book_id=book_id).filter_by(return_confirm = False).first()

      accept = request.form.get('tcs')

      if borrower.lender_confirm:
        flash('Book already being borrowed.', category='error')
        return redirect(url_for('views.status', book_id=book_id))    

      elif borrower_exists:
        flash('Borrower is already at limit (1/1)', category='error')
        return redirect(url_for('views.status', book_id=book_id))    


      elif not accept:
        flash('Please read and accept our terms and conditions!', category='error')

      else:

        requests.lender_confirm = True
        
        requests.borrowed_date = datetime.utcnow()
        
        due_date_set = timedelta(weeks = 2)
        due_date = datetime.utcnow() + due_date_set

        requests.due_date = due_date

        db.session.add(requests)
        db.session.commit()

        flash('Successfully confirmed! Now returning to dashboard', category='success')
        return redirect(url_for('views.status', book_id=book_id))    


  return render_template("accept.html", user=current_user, book=book, borrowerlist=borrowerlist, borrower_exists=borrower_exists)

@views.route('/returned/<int:book_id>/borrower/<int:borrower_id>', methods=['GET', 'POST'])
@login_required
def return_confirm(book_id, borrower_id):
  """
  This allows the lender to confirm that the borrower has returned the book
  """
  book = Book.query.get_or_404(book_id)

  requests = Borrowed_book.query.filter_by(borrower_id=borrower_id).filter_by(book_id=book_id).filter_by(return_confirm = False).first()

  borrowerlist = db.session.query(Borrower, Borrowed_book)\
    .filter(book_id == Borrowed_book.book_id)\
    .filter(borrower_id == Borrowed_book.borrower_id)\
    .outerjoin(Borrower, Borrower.id==Borrowed_book.borrower_id)\
    .add_columns(Borrower.username, Borrower.id, Borrowed_book.borrower_id, Borrower.fName, Borrower.lName, Borrower.address1, Borrower.city, Borrower.phone, Borrowed_book.lender_confirm, Borrowed_book.due_date)\
    .filter(Borrower.id == Borrowed_book.borrower_id).first()

  borrower_exists = db.session.query(Borrower, Borrowed_book)\
    .filter(borrower_id == Borrowed_book.borrower_id)\
    .filter(Borrowed_book.lender_confirm == True)\
    .outerjoin(Borrower, Borrower.id==Borrowed_book.borrower_id)\
    .filter(Borrower.id == Borrowed_book.borrower_id).first()

  if current_user.id != book.lender_user_id:
    abort(403)


  else:
    if request.method == 'POST':
      for borrower in borrowerlist:
        borrower = Borrowed_book.query.filter_by(borrower_id=borrower_id).filter_by(book_id=book_id).filter_by(return_confirm = False).first()

      if borrower.return_confirm:
        flash('Book already being borrowed.', category='error')
        return redirect(url_for('views.status', book_id=book_id))    

      elif borrower_exists:
        flash('Borrower is already at limit (1/1)', category='error')
        return redirect(url_for('views.status', book_id=book_id))    


      elif not accept:
        flash('Please read and accept our terms and conditions!', category='error')

      else:

        requests.return_confirm = True
        requests.lender_confirm = False

        db.session.add(requests)
        db.session.commit()

        flash('Successfully confirmed! Now returning to dashboard', category='success')
        return redirect(url_for('views.status', book_id=book_id))    

  return render_template("return_confirm.html", user=current_user, book=book, borrowerlist=borrowerlist)

@views.route('/return/<int:book_id>/borrower/<int:lender_id>', methods=['GET', 'POST'])
@login_required
def returned(book_id, lender_id):
  """
  This allows the borrower to notify the lender that they are going to return the book
  """
  book = Book.query.get_or_404(book_id)

  requests = Borrowed_book.query.filter_by(lender_id=lender_id).filter_by(book_id=book_id).filter_by(return_confirm = False).first()
  borrower = Borrower.query.filter_by(user_id=current_user.id).first()


  lenderlist = db.session.query(Lender, Borrowed_book)\
    .filter(book_id == Borrowed_book.book_id)\
    .filter(lender_id == Borrowed_book.lender_id)\
    .outerjoin(Lender, Lender.id==Borrowed_book.lender_id)\
    .add_columns(Lender.username, Lender.id, Borrowed_book.borrower_id, Lender.fName, Lender.lName, Lender.address1, Lender.city, Lender.phone, Borrowed_book.borrower_id, Borrowed_book.due_date, Borrowed_book.borrowed_date)\
    .filter(Lender.id == Borrowed_book.lender_id).first()

  if current_user.id != borrower.user_id:
    abort(403)


  else:
    if request.method == 'POST':
      
      if requests.return_book:
        flash('Lender already notifed.', category='error')
        return redirect(url_for('views.borrowed', user_id=current_user.id))    

      else:

        requests.return_book = True

        db.session.add(requests)
        db.session.commit()

        flash('Successfully confirmed! Refreshing page..', category='success')
        return redirect(url_for('views.borrowed', user_id=current_user.id))


  return render_template("return.html", user=current_user, book=book, lenderlist=lenderlist)

@views.route('/lenderdetails/<int:book_id>/lender/<int:lender_id>', methods=['GET', 'POST'])
@login_required
def lenderdetails(book_id, lender_id):
  """
  This allows the borrower to check the book's lender details
  """
  book = Book.query.get_or_404(book_id)

  borrower = Borrower.query.filter_by(user_id=current_user.id).first()


  lenderlist = db.session.query(Lender, Borrowed_book)\
    .filter(book_id == Borrowed_book.book_id)\
    .filter(lender_id == Borrowed_book.lender_id)\
    .outerjoin(Lender, Lender.id==Borrowed_book.lender_id)\
    .add_columns(Lender.username, Lender.id, Borrowed_book.borrower_id, Lender.fName, Lender.lName, Lender.address1, Lender.city, Lender.phone, Borrowed_book.borrower_id)\
    .filter(Lender.id == Borrowed_book.lender_id).first()

  if current_user.id != borrower.user_id:
    abort(403)

  return render_template("lender.html", user=current_user, book=book, lenderlist=lenderlist)


@views.route('/account/<int:user_id>', methods=['GET', 'POST'])
@login_required
def account(user_id):
  """
  This allows users to change their email or username
  """

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
  """
  This lets users reset their password
  """
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

@views.route('/account/personaldetails/<int:user_id>', methods=['GET', 'POST'])
@login_required
def infoedit(user_id):
  """
  This allows the users to edit their personal information
  """
  lender = Lender.query.filter_by(user_id=user_id).first()
  borrower = Borrower.query.filter_by(user_id=current_user.id).first()


  if current_user.id != user_id:
    abort(403)

  if request.method == "POST":
    fName = request.form.get('fName')
    lName = request.form.get('lName')
    address1 = request.form.get('address')
    city = request.form.get('city')
    phone = request.form.get('phone')
    accept = request.form.get('tcs')

    phone_check = Lender.query.filter_by(phone=phone).first()
    if current_user.details == False:

      if phone_check:
        flash('Phone number already in use!', category='error')
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
        elif len(phone) < 8:
          flash('Phone must be more than eight characters!', category='error')
        elif not accept:
          flash('Please read and accept our terms and conditions!', category='error')
        else:
          lender = Lender(fName=fName, lName=lName, address1=address1, city=city, username=current_user.username, email=current_user.email, phone=phone, user_id=current_user.id)

          borrower = Borrower(fName=fName, lName=lName, address1=address1, city=city, username=current_user.username, email=current_user.email, phone=phone, user_id=current_user.id)
          
          current_user.details = True


          db.session.add(lender)
          db.session.add(borrower)
          db.session.add(current_user)
          db.session.commit()

          flash('Personal Information sucessfully added!', category='success')


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
      elif len(phone) < 8:
        flash('Phone must be more than eight characters!', category='error')
      elif not accept:
        flash('Please read and accept our terms and conditions!', category='error')
      elif fName == lender.fName and lender.lName == lName and  lender.address1 == address1 and lender.city == city and lender.phone == phone:
        flash('Please edit to continue!', category='error')
      else:
        lender.fName = fName
        lender.lName = lName
        lender.address1 = address1
        lender.city = city
        lender.phone = phone

        borrower.fName = fName
        borrower.lName = lName
        borrower.address1 = address1
        borrower.city = city
        borrower.phone = phone
        

        db.session.add(borrower)
        db.session.add(lender)
        db.session.commit()

        flash('Personal Information sucessfully edited!', category='success')


  return render_template("dashboard/infoedit.html", user=current_user, lender=lender)


@views.route('/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit(book_id):
  """
  This page takes the book_id and edit title and/or author or delete the book
  """

  book = Book.query.get_or_404(book_id)

  if current_user.id != book.lender_user_id:
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
  """
  This allows the user to lend a book by inserting its title and author. 
  """
  if request.method == 'POST':
    
    book = Book.query.filter_by(lender_user_id=current_user.id).all()

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
      book = Book(title=title, author=author, lender_user_id=current_user.id, lender_username=current_user.username)
      db.session.add(book)
      db.session.commit()

      if current_user.details == True:
        flash('Book sucessfully added', category='success')
        return redirect(url_for('views.books'))

      else:
        flash('Please enter personal details!', category='success')
        return redirect(url_for('views.lendinfo', book_id = book.id))

  return render_template("lend.html", user=current_user)

@views.route('/lenddetails/<int:book_id>', methods=['GET', 'POST'])
@login_required
def lendinfo(book_id):
  """
  If the user hasn't inserted their personal details before lending a book, they redirect to this page to do so
  """

  books = Book.query.get_or_404(book_id)
  borrower = Borrower.query.filter_by(user_id=current_user.id).first()


  if current_user.id != books.lender_user_id:
    abort(403)
  elif current_user.details == True:
    abort(403)
  else:

    if request.method == 'POST':
      fName = request.form.get('fName')
      lName = request.form.get('lName')
      address1 = request.form.get('address')
      city = request.form.get('city')
      phone = request.form.get('phone')
      accept = request.form.get('tcs')


      phone_check = Lender.query.filter_by(phone=phone).first()

      if phone_check:
        flash('Phone number already in use!', category='error')
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
        elif len(phone) < 8:
          flash('Phone must be more than eight characters!', category='error')
        elif not accept:
          flash('Please read and accept our terms and conditions!', category='error')
        else:
          lender = Lender(fName=fName, lName=lName, address1=address1, city=city, username=current_user.username, email=current_user.email, phone=phone, user_id=current_user.id)
          borrower = Borrower(fName=fName, lName=lName, address1=address1, city=city, username=current_user.username, email=current_user.email, phone=phone, user_id=current_user.id)       
          
          current_user.details = True

          db.session.add(borrower)
          db.session.add(lender)
          db.session.add(current_user)
          db.session.commit()
          
          flash('Details added! Book Lended!', category='success')
          return redirect(url_for('views.books'))

    return render_template("lenddetails.html", user=current_user, book=books, borrower=borrower)

@views.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
@login_required
def borrow(book_id):
  """
  This allows users to borrow books without spamming requests.
  """
  books = Book.query.get_or_404(book_id)
  lender = Lender.query.filter_by(user_id=current_user.id).first()
  borrower = Borrower.query.filter_by(user_id=current_user.id).first()
  lender_id = Lender.query.filter_by(user_id = books.lender_user_id).first()

  if current_user.details:
    borrowed_before = Borrowed_book.query.filter_by(borrower_id = borrower.id).filter_by(book_id=book_id).filter_by(return_confirm = True).first()
    check_request = Borrowed_book.query.filter_by(borrower_id = borrower.id).filter_by(book_id=book_id).filter_by(return_confirm = False).first()

  try:
    requests = Borrowed_book.query.filter_by(book_id = book_id).first()

  except AttributeError: 
    if requests.lender_confirm == True:
      flash('Book already being borrowed. Please try again in the near future!', category='error')
      return redirect(url_for('views.books'))
  
  else:

    if current_user.id == books.lender_user_id:
      abort(403)
    elif not current_user.details:
      flash('Enter personal details!', category='error')
      return redirect(url_for('views.infoedit', user_id=current_user.id))
      
    if request.method == 'POST':
      fName = request.form.get('fName')

      lName = request.form.get('lName')
      address1 = request.form.get('address')
      city = request.form.get('city')
      phone = request.form.get('phone')
      accept = request.form.get('tcs')

      borrowed_before = Borrowed_book.query.filter_by(borrower_id = borrower.id).filter_by(book_id=book_id).filter_by(return_confirm = True).first()
      phone_check = Borrower.query.filter_by(phone=phone).first()
      check_request = Borrowed_book.query.filter_by(borrower_id = borrower.id).filter_by(book_id=book_id).filter_by(return_confirm = False).first()
      id = Borrower.query.filter_by(user_id=current_user.id).first()

      if current_user.details == False:
        if phone_check:
          flash('Phone number already in use!', category='error')
        elif check_request:
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
          elif len(phone) < 8:
            flash('Phone must be more than eight characters!', category='error')
          elif not accept:
            flash('Please read and accept our terms and conditions!', category='error')

          else:
            if not id:
              lender = Lender(fName=fName, lName=lName, address1=address1, city=city, username=current_user.username, email=current_user.email, phone=phone, user_id=current_user.id)
              new_borrower = Borrower(fName=fName, lName=lName, address1=address1, city=city, username=current_user.username, email=current_user.email, phone=phone, user_id=current_user.id)

              db.session.add(lender)
              db.session.add(new_borrower)
              db.session.commit()

      
              requests = Borrowed_book(return_book=False, return_confirm=False, lender_confirm=False, borrower_id=new_borrower.id, lender_id=lender_id.id,book_id=book_id)

              current_user.details = True
              
              db.session.add(current_user)

            else:
              requests = Borrowed_book(return_book=False, return_confirm=False, lender_confirm=False, borrower_id=borrower.id, lender_id=lender_id.id, book_id=book_id)

            db.session.add(requests)
            db.session.commit()
            
            flash('Details Added. Lender notifed, please wait for response!', category='success')
            return redirect(url_for('views.books'))

      else:

        if fName != borrower.fName and borrower.lName != lName and  borrower.address1 != address1 and borrower.city != city and borrower.phone != phone:
          if phone_check:
            flash('Phone number already in use!', category='error')
          elif check_request:
            flash('Request already sent!', category='error')
            return redirect(url_for('views.books')) 
          else:
            if not id:
              lender = Lender(fName=fName, lName=lName, address1=address1, city=city, username=current_user.username, email=current_user.email, phone=phone, user_id=current_user.id)
              new_borrower = Borrower(fName=fName, lName=lName, address1=address1, city=city, username=current_user.username, email=current_user.email, phone=phone, user_id=current_user.id)

              db.session.add(lender)
              db.session.add(new_borrower)
              db.session.commit()

              
              requests = Borrowed_book(return_book=False, return_confirm=False, lender_confirm=False, borrower_id=new_borrower.id, lender_id=lender_id.id,book_id=book_id)

              current_user.details = True
              
              db.session.add(current_user)

            else:
              requests = Borrowed_book(return_book=False, return_confirm=False, lender_confirm=False, borrower_id=borrower.id, lender_id=lender_id.id, book_id=book_id)

            db.session.add(requests)
            db.session.commit()
            
            flash('Details Added. Lender notifed, please wait for response!', category='success')
            return redirect(url_for('views.books'))

        else:
          if not id:
            lender = Lender(fName=fName, lName=lName, address1=address1, city=city, username=current_user.username, email=current_user.email, phone=phone, user_id=current_user.id)
            new_borrower = Borrower(fName=fName, lName=lName, address1=address1, city=city, username=current_user.username, email=current_user.email, phone=phone, user_id=current_user.id)

            db.session.add(lender)
            db.session.add(new_borrower)
            db.session.commit()

            
            requests = Borrowed_book(return_book=False, return_confirm=False, lender_confirm=False, borrower_id=new_borrower.id, lender_id=lender_id.id,book_id=book_id)

            current_user.details = True
            
            db.session.add(current_user)

          elif check_request:
            flash('Request already sent!', category='error')
            return redirect(url_for('views.books')) 

          else:
            requests = Borrowed_book(return_book=False, return_confirm=False, lender_confirm=False, borrower_id=borrower.id, lender_id=lender_id.id, book_id=book_id)

          db.session.add(requests)
          db.session.commit()
          
          flash('Details Added. Lender notifed, please wait for response!', category='success')
          return redirect(url_for('views.books'))

  return render_template("borrow.html", user=current_user, book=books, requests=requests, lender=lender, borrowed_before=borrowed_before)
