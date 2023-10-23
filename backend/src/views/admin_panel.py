from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required
from webargs.flaskparser import parser

from src.schemas.administration import login_post
from src.lib.access import allow_view
from src.db.models import User
from . import bp_admin

@bp_admin.errorhandler(422)
def handle_unprocessable_entity(err):
    return jsonify({
        'text': 'Не все поля были заполнены'
    }), 422

@bp_admin.errorhandler(401)
def handle_unauthorized_user(err):
    return redirect(url_for('bp_admin.login'))


@bp_admin.route('/')
@login_required
@allow_view(["admin"])
def index():
    return render_template('admin_panel/index.html')


@bp_admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = parser.parse(login_post, request)
        user = User.query.filter(User.roles.any(name='admin')).filter_by(email=data.get('email'), is_deleted=False).first()
        if not user:
            return render_template('admin_panel/login.html', err_msg='Пользователь с таким email не существует')
        if not user.verify_password(data.get('password')):
            return render_template('admin_panel/login.html', err_msg='Неверный email или пароль')
        login_user(user)
        return redirect(url_for('bp_admin.index'))

    return render_template('admin_panel/login.html', err_msg=None)


@bp_admin.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('bp_admin.login'))
