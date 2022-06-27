import genericpath
import json
from os import path

import flask
from flask import Flask, render_template, Response, request

from settings.config import DefaultConfig

app = Flask(__name__)
CONFIG = DefaultConfig()


def create_app():
    app.register_error_handler(404, page_not_found)
    app.config['SECRET_KEY'] = CONFIG.SECRET_KEY

    # Import Blueprints
    from .views import views
    from .auth import auth
    # Registration of blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app


def page_not_found(e):
    return render_template('404.html'), 404


