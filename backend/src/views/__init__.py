"""Initialization API."""
from flask import Blueprint, render_template, request, redirect, url_for

from src.db import session, db


bp_front = Blueprint('bp_front', __name__)

@bp_front.route("/")
def index():
    return render_template('account.html', title='dpd')


bp_admin = Blueprint('bp_admin', __name__)

# bp_short_url = Blueprint('bp_short_url', __name__)

from src.views import service_params
from src.views import admin_panel
from src.views import users
from src.views import user_text_store







