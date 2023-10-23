from flask import render_template, jsonify
from flask_login import login_required
from webargs.flaskparser import  use_args

from src.schemas.administration import promo_codes_updates_post
from src.db import session
from src.db.models import ServiceParams, PromoCodes, PromoCodesOrders
from src.lib.access import allow_view
from . import bp_admin

@bp_admin.route('/promo_codes')
@login_required
@allow_view(["admin"])
def promo_codes():
    codes = PromoCodes.query.order_by(PromoCodes.active.desc(), PromoCodes.created_at.desc()).all()
    codes_list = list()
    if codes:
        for code in codes:
            codes_data = {
                'id': code.id,
                'code': code.code,
                'started_at': code.started_at,
                'ends_at': code.ends_at,
                'price': code.price,
                'min_price': code.min_price,
                'max_price': code.max_price,
                'order_type': code.order_type,
                'active': code.active,
            }
            if code.type:
                code_type = ServiceParams.query.filter_by(id=code.type).first()
                if code_type:
                    codes_data.update({
                        'type': code_type.u_name
                    })
            codes_list.append(codes_data)

    params = {'device_type' : []}
    name_param_vals = []
    for name_param in ['device_type', 'accessories_device']:
        service_params = ServiceParams.query.filter(ServiceParams.parent.has(u_name=str(name_param))).all()
        for service_param in service_params:
            if not service_param.deprecated and service_param.u_name not in ['models_samsung', 'accessories_device', 'models_huawei', 'models_iphones_repair']:
                name_param_vals.append({
                    'name': service_param.name,
                    'val': service_param.u_name
                })
    if name_param_vals:
        params['device_type'] = name_param_vals
    return render_template('admin_panel/promo_codes.html', params=params, codes_list=codes_list)


@bp_admin.route('/promo_codes/updates', methods=['POST'])
@login_required
@allow_view(["admin"])
@use_args(promo_codes_updates_post)
def promo_codes_updates(data):
    if not data.get('new_entries') and not data.get('changed_entries') and not data.get('deprecated_entries') and not data.get('respawn_entries') and not data.get('purge_entries') and not data.get('promocode_date'):
        return jsonify({
            'text': 'Изменения отсутствуют'
        }), 422

    if data.get('promocode_date'):
        all_promo_codes = PromoCodes.query.all()
        for promo_code in all_promo_codes:
            promo_code.ends_at = data.get('promocode_date')

    if data.get('new_entries'):
        
        for entry in data.get('new_entries'):
            new_code = PromoCodes()
            for item in entry.items():
                if item[0] == 'device_type':
                    if item[1]:
                        param = ServiceParams.get_by_uname(item[1], group='device_type')
                        if not param:
                            param = ServiceParams.get_by_uname(item[1], group='accessories_device')
                        if param:
                            new_code.type = param.id
                    else:
                        new_code.type = None
                if item[0] == 'code':
                    new_code.code = item[1]
                if item[0] == 'started_at':
                    new_code.started_at = item[1] if item[1] else None
                if item[0] == 'ends_at':
                    new_code.ends_at = item[1] if item[1] else None
                if item[0] == 'price':
                    new_code.price = item[1]
                if item[0] == 'min_price':
                    new_code.min_price = item[1] if item[1] else None
                if item[0] == 'max_price':
                    new_code.max_price = item[1] if item[1] else None
                if item[0] == 'order_type':
                    new_code.order_type = item[1] if item[1] else None
            session.add(new_code)

    if data.get('changed_entries'):
        for entry in data.get('changed_entries'):
            code = PromoCodes.query.get(str(entry.get('code_id')))
            if not code:
                return jsonify({
                    'text': 'Ошибка при редактировании одной из записей (не найден идентификатор)'
                }), 404
            for item in entry.items():
                if item[0] == 'device_type':
                    if item[1]:
                        param = ServiceParams.get_by_uname(item[1], group='device_type')
                        if not param:
                            param = ServiceParams.get_by_uname(item[1], group='accessories_device')
                        if param:
                            code.type = param.id
                    else:
                        code.type = None
                if item[0] == 'code':
                    code.code = item[1]
                if item[0] == 'started_at':
                    code.started_at = item[1] if item[1] else None
                if item[0] == 'ends_at':
                    code.ends_at = item[1] if item[1] else None
                if item[0] == 'price':
                    code.price = item[1]
                if item[0] == 'min_price':
                    code.min_price = item[1] if item[1] else None
                if item[0] == 'max_price':
                    code.max_price = item[1] if item[1] else None
                if item[0] == 'order_type':
                    code.order_type = item[1] if item[1] else None

    if data.get('deprecated_entries'):
        for entry in data.get('deprecated_entries'):
            code = PromoCodes.query.get(str(entry.get('code_id')))
            if not code:
                return jsonify({
                    'text': 'Ошибка при редактировании одной из записей (не найден идентификатор)'
                }), 404
            code.active = False

    if data.get('respawn_entries'):
        for entry in data.get('respawn_entries'):
            code = PromoCodes.query.get(str(entry.get('code_id')))
            if not code:
                return jsonify({
                    'text': 'Ошибка при редактировании одной из записей (не найден идентификатор)'
                }), 404
            code.active = True

    if data.get('purge_entries'):
        for entry in data.get('purge_entries'):
            code = PromoCodes.query.get(str(entry.get('code_id')))
            if not code:
                return jsonify({
                    'text': 'Ошибка при удалении одной из записей (не найден идентификатор)'
                }), 404
            orders = PromoCodesOrders.query.filter_by(promo_code_id=str(entry.get('code_id'))).first()
            if orders:
                return jsonify({
                    'text': 'Один из выбранных элементов не может быть удален тк уже используеться (можете воспользоваться пунктом УСТАРЕЛО)'
                }), 403

            session.delete(code)

    session.commit()

    return jsonify({})