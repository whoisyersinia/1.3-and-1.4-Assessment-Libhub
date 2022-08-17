from website import db
from flask_login import UserMixin
from datetime import datetime
class User(db.Model, UserMixin):

  __tablename__ = 'user'

  id = db.Column(
    db.Integer, 
    primary_key=True
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

  # user_email = db.relationship(
  #   "user_email",
  #   uselist=False,
  #   backref='user',
  #   lazy=True
  # )

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()


# class Borrower(db.Model):

#   __tablename__ = 'borrower'

#   idborrower= db.Column(
#     db.Integer,
#     primary_key=True
#   )

#   fName = db.Column(
#     db.String(150),
#     unique=False,
#     nullable=False
#   )
    
#   lName = db.Column(
#     db.String(150),
#     unique=False,
#     nullable=False
#   )
  
#   address1 = db.Column(
#     db.String(150),
#     nullable=False
#   )

#   address2 = db.Column(
#     db.String(150),
#     nullable=True
#   )

#   city = db.Column(
#     db.String(80),
#     nullable=True
#   )

#   phone = db.Column(
#     db.Integer,
#     unique=True,
#     nullable=True
#   )

#   user_email = db.Column(
#     db.String(150),
#     db.ForeignKey('user.email'),
#     nullable=False
#   )

#   user_id = db.Column(
#     db.Integer,
#     db.ForeignKey('user.id'),
#     nullable=False
#   )

#   borrower_id = db.relationship(
#     "Borrowed_book",
#     backref='borrower',
#     lazy=True
#   )


# class Borrowed_book(db.Model):

#   __tablename__ =' borrowed_book'

#   idloan = db.Column(
#     db.Integer,
#     primary_key=True
#   )

#   borrowed_date = db.Column(
#     db.DateTime,
#     unique=False,
#     nullable=False,
#     default=datetime.utcnow
#   )

#   # due_date = db.Column(
#   #   db.Date('now', 'start of month', '+14 days'),
#   #   nullable=False,
#   #   unique=False
#   # )

#   return_book = db.Column(
#     db.Boolean,
#     nullable=False,
#     default=False
#   )

#   borrower_id = db.Column(
#     db.Integer,
#     db.ForeignKey('borrower.idborrower'),
#     nullable=False
#   )

#   book_id = db.Column(
#     db.Integer,
#     db.ForeignKey('book.idbooks'),
#     nullable=False
#   )

# class Book(db.Model):

#   __tablename__ = 'book'


#   idbooks = db.Column(
#     db.Integer,
#     primary_key=True
#   )

#   title = db.Column(
#     db.String(256),
#     nullable=False,
#     unique=False
#   )

#   author = db.Column(
#     db.String(256),
#     nullable=False,
#     unique=False,
#     default='Anonymous'
#   )

#   isbn_no = db.Column(
#     db.Integer,
#     nullable=False
#   )

#   book_id = db.relationship(
#     "Book",
#     backref='book',
#     lazy=True
#   )

#   lender_id = db.Column(
#     db.Integer,
#     db.ForeignKey('lender.idlender'),
#     nullable=False
#   )

# class Lender(db.Model):

#   __tablename__ = 'lender'

#   idlender= db.Column(
#     db.Integer,
#     primary_key=True
#   )

#   fName = db.Column(
#     db.String(150),
#     unique=False,
#     nullable=False
#   )
    
#   lName = db.Column(
#     db.String(150),
#     unique=False,
#     nullable=False
#   )
  
#   address1 = db.Column(
#     db.String(150),
#     nullable=False
#   )

#   address2 = db.Column(
#     db.String(150),
#     nullable=True
#   )

#   city = db.Column(
#     db.String(80),
#     nullable=True
#   )

#   phone = db.Column(
#     db.Integer,
#     unique=True,
#     nullable=True
#   )

#   user_email = db.Column(
#     db.String(150),
#     db.ForeignKey('user.email'),
#     nullable=False
#   )

#   user_id = db.Column(
#     db.Integer,
#     db.ForeignKey('user.id'),
#     nullable=False
#   )

#   lender_id = db.relationship(
#     "lender_book",
#     backref='lender',
#     lazy=True
#   )



