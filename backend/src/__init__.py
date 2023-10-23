"""Initialization of all codebase."""
import logging, json
from flask import Flask, request, g
from flask_cors import CORS

from src.api import bp_app
from src.db import db
from src.lib.access import login_manager
from src.lib.sending import internal_error_notification, mail
from src.views import bp_front
from src.views import bp_admin


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    login_manager.init_app(app)
    CORS(app)
    db.init_app(app)
    mail.init_app(app)

    if app.config['DEBUG']:
        @app.after_request
        def after(resp):
            if resp.status_code >= 400:
                print(resp.get_data().decode())
            return resp
    else:
        @app.after_request
        def internal_error(resp):
            if resp.status_code >= 500:
                print('=-=-= RECIEVED DATA =-=-=')
                print(request.data.decode())
                print('=-=-=-=-=-=-=-=-=-=--=-=-=')
                failed_user = str(g.current_user.id) if g.current_user and g.current_user.id else 'Anon'
                internal_error_notification(failed_user)
            return resp

    app.register_blueprint(bp_app, url_prefix='/api')
    app.register_blueprint (bp_front, url_prefix='/account')
    app.register_blueprint (bp_admin, url_prefix='/admin')
    # app.register_blueprint (bp_short_url, url_prefix='/short-url')

    return app
