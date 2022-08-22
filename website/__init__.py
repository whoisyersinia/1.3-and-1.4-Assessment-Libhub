import re
from os import path
from flask import Flask
from sassutils.wsgi import SassMiddleware
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '79fbb45b557f4402167be70f8c8820c05d4047255c8dc29a'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)



    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    app.wsgi_app = SassMiddleware(
        app.wsgi_app,
        {
            'website': {
                'sass_path': 'static/sass',
                'css_path': 'static/css',
                'wsgi_path': '/static/css',
                'strip_extension': False
            }
        }
    )

    @app.before_first_request
    def create_tables():
        from .models import User
        db.create_all()

    from .models import User, Borrower, Borrowed_book, Book

    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
    
    