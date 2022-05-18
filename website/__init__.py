import genericpath
from os import path

from flask import Flask, render_template

from settings.config import DefaultConfig

CONFIG = DefaultConfig()

def create_app():
    app = Flask(__name__)
    app.register_error_handler(404, page_not_found)
    app.config['SECRET_KEY'] = CONFIG.SECRET_KEY

    # Import Blueprints
    from .views import views
    from .auth import auth
    # Registrazione delle Blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

def page_not_found(e):
    return render_template('404.html'), 404