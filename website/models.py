from enum import unique
from website import db
from flask_login import UserMixin

#books table
class User(db.Model, UserMixin):
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
    index=False,
    unique=False,
    nullable=True
  )

  def save_to_db(self):
        db.session.add(self)
        db.session.commit()


  # fName = db.Column(db.String(150))
  # lName = db.Column(db.String(150))

