from website import create_app

DB_NAME = 'database.db'

SECRET_KEY = '79fbb45b557f4402167be70f8c8820c05d4047255c8dc29a'
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
