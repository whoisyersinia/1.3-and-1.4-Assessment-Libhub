import re
from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
  return render_template("index.html")

@views.route('/books')
def books():
  return render_template("books.html")