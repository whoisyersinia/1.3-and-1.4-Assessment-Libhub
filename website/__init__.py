import sqlite3
from flask import Flask
from sassutils.wsgi import SassMiddleware

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '79fbb45b557f4402167be70f8c8820c05d4047255c8dc29a'

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
    

    return app
    
    