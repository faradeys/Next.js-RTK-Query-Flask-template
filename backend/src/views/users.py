import re
from flask import render_template, jsonify
from flask_login import login_required
from webargs.flaskparser import use_args

from src.schemas.administration import user_info_post, user_updates_post, password_update
from src.db import session
from src.db.models import User
from src.lib.utils import parse_phone
from src.lib.access import allow_view
from src.views import bp_admin


@bp_admin.route('/users', methods=['GET'])
@login_required
@allow_view(["admin"])
def users():
    return render_template('admin_panel/users.html')


@bp_admin.route('/users', methods=['POST'])
@login_required
@allow_view(["admin"])
@use_args(user_info_post)
def users_info(data):
    if not data.get('search_str') and not data.get('search_id_str'):
        search_fail = True
        return render_template('admin_panel/users.html', search_fail=search_fail)

    if data.get('search_str'):
        if re.search(r'(FB:|VK:)', data.get('search_str')):
            users = User.query.filter_by(side_id=data.get('search_str')).all()
        else:
            users = User.query.filter_by(phone=parse_phone(data.get('search_str')), is_verified=True).all()

    if data.get('search_id_str'):
        users = User.query.filter_by(id=data.get('search_id_str')).all()

    users_list = list()
    search_fail = False
    pass_change = False
    if users:
        for user in users:
            referrer = User.query.get(user.referrers_id) if user.referrers_id else None
            users_list.append({
                'id': user.id,
                'phone': user.phone,
                'side_id': user.side_id,
                'name': user.name,
                'city': user.city,
                'email': user.email,
                'bonuses': user.bonuses,
                'created_at': user.created_at
            })
        pass_change = True
    else:
        search_fail = True

    return render_template('admin_panel/users.html', users_list=users_list, search_fail=search_fail, pass_change=pass_change)


@bp_admin.route('/users/updates', methods=['POST'])
@login_required
@allow_view(["admin"])
@use_args(user_updates_post)
def users_updates(data):
    if not data.get('changed_entries'):
        return jsonify({
            'text': 'Изменения отсутствуют'
        }), 422

    if data.get('changed_entries'):
        for entry in data.get('changed_entries'):
            user = User.query.get(str(entry.get('user_id')))
            if not user:
                return jsonify({
                    'text': 'Ошибка при редактировании одной из записей (не найден идентификатор)'
                }), 422

            if not user.side_id and not entry.get('phone'):
                return jsonify({
                    'text': 'У пользователя должен присутствовать номер телефона, если он не авторизован через соц.сети'
                }), 422

            for item in entry.items():
                if item[0] == 'phone':
                    user.phone = item[1]
                if item[0] == 'name':
                    user.name = item[1]
                if item[0] == 'city':
                    user.city = item[1]
                if item[0] == 'email':
                    user.email = item[1]
                if item[0] == 'bonuses':
                    user.bonuses = item[1]

    session.commit()

    return jsonify({})

@bp_admin.route('/users/new_pass', methods=['POST'])
@login_required
@allow_view(["admin"])
@use_args(password_update)
def password_update(data):
    user = User.query.filter_by(phone=data.get('user_phone')).first()
    user.hash_password(data.get('new_pass'))

    session.commit()

    return jsonify({})