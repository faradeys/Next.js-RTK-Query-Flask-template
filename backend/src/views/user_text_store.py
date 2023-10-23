from flask import render_template, redirect, url_for, request
from flask_login import login_required

from src.db.models import UserTextStore
from src.lib.access import allow_view
from . import bp_admin

@bp_admin.route('/user_text_store')
@login_required
@allow_view(["admin"])
def user_text_store():
    per_page = request.args.get("per_page", 20, type=int)
    page = request.args.get("page", 1, type=int)
    user_texts_paginate = UserTextStore.query.order_by(UserTextStore.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    if page > user_texts_paginate.pages:
        return redirect(url_for('bp_admin.user_text_store'))

    user_texts_list = list()

    if user_texts_paginate:
        for user_data in user_texts_paginate.items:
            user_texts_list.append({
                'phone': user_data.phone if user_data.phone else '-',
                'name': user_data.name if user_data.name else '-',
                'email': user_data.email if user_data.email else '-',
                'text': user_data.text if user_data.text else '-',
                'created_at': user_data.created_at.strftime("%H:%M:%S %d-%m-%Y ") if user_data.created_at else '-',
            })

    return render_template('admin_panel/user_text_store.html', user_texts_list=user_texts_list, user_texts_paginate=user_texts_paginate, cur_page=page, per_page=per_page)
