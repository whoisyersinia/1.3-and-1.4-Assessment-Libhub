import re
from os import path
from flask import Flask, render_template, request, url_for
from sassutils.wsgi import SassMiddleware
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import views
    from .auth import auth
    from .handlers import errors

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(errors, url_prefix="/")

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
        from .models import User, Borrower, Borrowed_book, Lender, Book
        db.create_all()

    from .models import User, Borrower, Borrowed_book, Lender, Book
    
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
    
    