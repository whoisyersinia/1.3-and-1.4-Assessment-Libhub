from xmlrpc.client import DateTime
from website import db
from flask_login import UserMixin
from datetime import datetime
class Book(db.Model):

  __tablename__ = 'book'

  id = db.Column(
    db.Integer,
    primary_key=True
  )

  title = db.Column(
    db.String(255),
    nullable=False,
    unique=False
  )

  author = db.Column(
    db.String(255),
    nullable=False,
    unique=False,
    default='Anonymous'
  )

  created_on = db.Column(
    db.DateTime,
    unique=False,
    nullable=False,
    default=datetime.utcnow
  )

  lender_id= db.Column(
    db.Integer,
    db.ForeignKey('lender.id'),
    nullable=False
  )

  lender_username=db.Column(
    db.String(15),
    nullable=False,
  )

class Borrower(db.Model):

  __tablename__ = 'borrower'

  id= db.Column(
    db.Integer,
    primary_key=True
  )

  fName = db.Column(
    db.String(150),
    unique=False,
    nullable=False
  )
    
  lName = db.Column(
    db.String(150),
    unique=False,
    nullable=False
  )
  
  address1 = db.Column(
    db.String(150),
    nullable=False
  )

  address2 = db.Column(
    db.String(150),
    nullable=True
  )

  city = db.Column(
    db.String(80),
    nullable=True
  )

  email = db.Column(
    db.String(150), 
    unique=True,
    nullable=False
  )

  username = db.Column(
    db.String(15), 
    unique=True,
    nullable=False
  )

  phone = db.Column(
    db.Integer,
    unique=True,
    nullable=True
  )

  user_id = db.Column(
    db.Integer,
    db.ForeignKey('user.id'),
    nullable=False
  )

  borrower_id = db.relationship(
    "Borrowed_book",
    backref='borrower',
    lazy=True
  )

class Lender(db.Model):

  __tablename__ = 'lender'

  id=db.Column(
    db.Integer,
    primary_key=True
  )

  fName = db.Column(
    db.String(150),
    nullable=False
  )
    
  lName = db.Column(
    db.String(150),
    unique=False,
    nullable=False
  )
  
  address1 = db.Column(
    db.String(150),
    nullable=False
  )

  address2 = db.Column(
    db.String(150),
    nullable=True
  )

  city = db.Column(
    db.String(80),
    nullable=True
  )

  email = db.Column(
    db.String(150), 
    unique=True,
    nullable=False
  )
  
  username = db.Column(
    db.String(15), 
    unique=True,
    nullable=False
  )

  phone = db.Column(
    db.Integer,
    unique=True,
    nullable=True
  )

  user_id = db.Column(
    db.Integer,
    db.ForeignKey('user.id'),
    nullable=False
  )

  lender_id = db.relationship(
    "Book",
    backref='lender',
    lazy=True
  )


class Borrowed_book(db.Model):

  __tablename__ = 'borrowed_book'

  id = db.Column(
    db.Integer,
    primary_key=True
  )

  borrowed_date = db.Column(
    db.DateTime,
    unique=False,
    nullable=False,
    default=datetime.utcnow
  )

  due_date = db.Column(
    db.DateTime,
    nullable=False,
    unique=False,
    default=datetime.utcnow
  )

  return_book = db.Column(
    db.Boolean,
    nullable=False,
    default=False
  )

  lender_confirm = db.Column(
    db.Boolean,
    nullable=False,
    default=False
  )

  borrower_id = db.Column(
    db.Integer,
    db.ForeignKey('borrower.id'),
    nullable=False
  )

  book_id = db.Column(
    db.Integer,
    db.ForeignKey('book.id'),
    nullable=False
  )


class User(db.Model, UserMixin):

  __tablename__ = 'user'

  id = db.Column(
    db.Integer, 
    primary_key=True
  )

  username = db.Column(
    db.String(15), 
    unique=True,
    nullable=False
  )
  
  email = db.Column(
    db.String(150), 
    unique=True,
    nullable=False
  )
  password = db.Column(
    db.String(150),
    nullable=False
  )
  created_on = db.Column(
    db.DateTime,
    unique=False,
    nullable=False,
    default=datetime.utcnow
  )

  user_id = db.relationship(
    "Borrower",
    backref='user',
    lazy=True
  )





