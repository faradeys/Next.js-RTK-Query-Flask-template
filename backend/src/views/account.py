from flask import Blueprint, render_template, url_for, current_app

mod = Blueprint('account', __name__)

@mod.route("/")
def index():
    dev_server = current_app.config['DEBUG']
    return render_template('account.html',
        dev_server=dev_server,
        title='dpd')
