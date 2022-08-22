from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user
from . import db
from .models import User, Borrowed_book, Book, Borrower, Lender


views = Blueprint('views', __name__)

@views.route('/')
def home():
  return render_template("index.html", user=current_user)

@views.route('/books')
def books():
  books = Book.query.all()
  return render_template("books.html", user=current_user, books=books)

@views.route('/book/<path:book_title>/')
def search(book_title):
  book = Book.query.get_or_404(book.title)
  return render_template('search.html', book=book)

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
   return render_template("dashboard.html", user=current_user)

@views.route('/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit(book_id):

  book = Book.query.get_or_404(book_id)

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
        flash('Please try again to confirm!', category='error')
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
    else:
      book = Book(title=title, author=author, lender_id=current_user.id)
      db.session.add(book)
      db.session.commit()

      flash('Book sucessfully added', category='success')
      return redirect(url_for('views.books'))




  return render_template("lend.html", user=current_user)

@views.route('/borrow', methods=['GET', 'POST'])
@login_required
def borrow():
  return render_template("borrow.html", user=current_user)