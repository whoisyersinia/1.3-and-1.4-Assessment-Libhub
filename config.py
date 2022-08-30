import os
from website import db

DB_NAME = 'database.db'

SECRET_KEY = '79fbb45b557f4402167be70f8c8820c05d4047255c8dc29a'
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']
MAIL_DEFAULT_SENDER = 'noreply.libhub@gmail.com'