from flask import render_template, jsonify, redirect, url_for
from flask_login import login_required
from webargs.flaskparser import use_args
from sqlalchemy import exc

from src.schemas.administration import service_params_updates_post
from src.db import session
from src.db.models import ServiceParams
from src.lib.access import validate_uuid, allow_view
from . import bp_admin


@bp_admin.route('/service_params')
@login_required
@allow_view(["admin"])
def service_params():
    main_ser_pars_list = list()
    ser_pars = ServiceParams.query.filter(ServiceParams.parent_id==None).all()
    ser_pars_list = dict()
    if ser_pars:
        ser_pars_list = [{
            'id': ser_par.id,
            'parent': ser_par.parent.id if ser_par.parent else None,
            'name': ser_par.name,
            'u_name': ser_par.u_name,
            'spec_value': ser_par.spec_value if ser_par.spec_value else '',
            'deprecated': 1 if ser_par.deprecated else 0,
            'created_at': ser_par.created_at
        } for ser_par in ser_pars]
        ser_pars_list.sort(key=lambda x: x['u_name'], reverse=False)
        ser_pars_list.sort(key=lambda x: x['created_at'], reverse=True)
        ser_pars_list.sort(key=lambda x: x['deprecated'], reverse=False)
        main_ser_pars_list.append({
            'device': 'без родителей',
            'ser_pars_list': ser_pars_list
        })

    params = dict()
    service_params = ServiceParams.query.filter_by(deprecated=False).all()
    if service_params:
        param_vals = []
        for service_param in service_params:
            if not service_param.deprecated:
                param_vals.append({
                    'name': service_param.parent.name+': '+service_param.name+' ('+service_param.u_name+')' if service_param.parent else str(service_param.name)+' ('+str(service_param.u_name)+')',
                    'id': service_param.id
                })
        if param_vals:
            params.update({'parent': param_vals})

    main_parent_params = list()
    service_params = ServiceParams.query.filter(ServiceParams.childs!=None, ServiceParams.deprecated==False).order_by(ServiceParams.name.asc()).all()
    if service_params:
        main_parent_params = [{
            'name': service_param.parent.name+': '+service_param.name+' ('+service_param.u_name+')' if service_param.parent else service_param.name+' ('+service_param.u_name+')',
            'id': service_param.id
        } for service_param in service_params]
    return render_template('admin_panel/service_params.html', main_parent_params=main_parent_params, params=params, main_ser_pars_list=main_ser_pars_list)


@bp_admin.route('/service_params/<main_group_uuid>')
@login_required
@allow_view(["admin"])
def service_params_group(main_group_uuid):
    if not validate_uuid(main_group_uuid):
        return redirect(url_for('bp_admin.service_params'))

    group_ser_pars = ServiceParams.query.get(str(main_group_uuid))
    main_ser_pars_list = list()
    ser_pars_list = list()
    if group_ser_pars and group_ser_pars.childs:
        for ser_pars in group_ser_pars.childs:
            ser_pars_list.append({
                'id': ser_pars.id,
                'parent': ser_pars.parent.id if ser_pars.parent else None,
                'name': ser_pars.name,
                'u_name': ser_pars.u_name,
                'spec_value': ser_pars.spec_value if ser_pars.spec_value else '',
                'deprecated': 1 if ser_pars.deprecated else 0,
                'created_at': ser_pars.created_at
            })
        ser_pars_list.sort(key=lambda x: x['u_name'], reverse=False)
        ser_pars_list.sort(key=lambda x: x['created_at'], reverse=True)
        ser_pars_list.sort(key=lambda x: x['deprecated'], reverse=False)
        main_ser_pars_list.append({
            'device': group_ser_pars.name,
            'ser_pars_list': ser_pars_list
        })

    params = dict()
    service_params = ServiceParams.query.filter_by(deprecated=False).all()
    if service_params:
        param_vals = []
        for service_param in service_params:
            if not service_param.deprecated:
                param_vals.append({
                    'name': service_param.parent.name + ': ' + service_param.name + ' (' + service_param.u_name + ')' if service_param.parent else service_param.name + ' (' + service_param.u_name + ')',
                    'id': service_param.id
                })
        if param_vals:
            params.update({'parent': param_vals})

    main_parent_params = list()
    service_params = ServiceParams.query.filter(ServiceParams.childs != None, ServiceParams.deprecated == False).order_by(ServiceParams.name.asc()).all()
    if service_params:
        main_parent_params = [{
            'name': service_param.parent.name + ': ' + service_param.name + ' (' + service_param.u_name + ')' if service_param.parent else service_param.name + ' (' + service_param.u_name + ')',
            'id': service_param.id
        } for service_param in service_params]

    return render_template('admin_panel/service_params.html', main_parent_params=main_parent_params, params=params, main_ser_pars_list=main_ser_pars_list, main_group_id=group_ser_pars.id)


@bp_admin.route('/service_params/fines/<main_group_name>')
@login_required
@allow_view(["admin"])
def service_params_fines(main_group_name):
    main_group_ser_pars = ServiceParams.query.filter_by(u_name=str(main_group_name)).first()
    main_ser_pars_list = list()
    if main_group_ser_pars:
        device_list = list()
        if main_group_ser_pars.spec_value=='inherit':
            [device_list.append(x) for x in main_group_ser_pars.childs]
        else:
            device_list.append(main_group_ser_pars)

        for device in device_list:
            ser_pars_list = list()
            for group_ser_pars in device.childs:
                if group_ser_pars.childs and group_ser_pars.u_name not in ['serviced_battery_models', 'restored_display_iphone_fines']:
                    for ser_pars in group_ser_pars.childs:
                        ser_pars_list.append({
                            'id': ser_pars.id,
                            'parent': ser_pars.parent.id if ser_pars.parent else None,
                            'name': ser_pars.name,
                            'u_name': ser_pars.u_name,
                            'spec_value': ser_pars.spec_value if ser_pars.spec_value else '',
                            'deprecated': 1 if ser_pars.deprecated else 0,
                            'created_at': ser_pars.created_at
                        })
            ser_pars_list.sort(key=lambda x: x['u_name'], reverse=False)
            ser_pars_list.sort(key=lambda x: x['created_at'], reverse=True)
            ser_pars_list.sort(key=lambda x: x['deprecated'], reverse=False)
            main_ser_pars_list.append({
                'device': device.name,
                'ser_pars_list': ser_pars_list
            })

    params = dict()
    service_params = ServiceParams.query.filter_by(deprecated=False).all()
    if service_params:
        params.update({
            'parent': [{
                'name': service_param.parent.name + ': ' + service_param.name + ' (' + service_param.u_name + ')' if service_param.parent else service_param.name + ' (' + service_param.u_name + ')',
                'id': service_param.id
            } for service_param in service_params]
        })

    return render_template('admin_panel/service_params.html', params=params, main_ser_pars_list=main_ser_pars_list, main_group_name=main_group_ser_pars.name)


@bp_admin.route('/service_params/updates', methods=['POST'])
@login_required
@allow_view(["admin"])
@use_args(service_params_updates_post)
def service_params_updates(data):
    if not data.get('new_entries') and not data.get('changed_entries') and not data.get('deprecated_entries') and not data.get('respawn_entries') and not data.get('purge_entries'):
        return jsonify({
            'text': 'Изменения отсутствуют'
        }), 422

    if data.get('new_entries'):
        for entry in data.get('new_entries'):
            new_ser_par = ServiceParams()
            for item in entry.items():
                if item[0] == 'parent':
                    if not item[1]:
                        new_ser_par.parent_id = None
                    else:
                        param = ServiceParams.query.get(str(item[1]))
                        if param:
                            new_ser_par.parent = param
                if item[0] == 'name':
                    new_ser_par.name = item[1]
                if item[0] == 'u_name':
                    new_ser_par.u_name = item[1]
                if item[0] == 'spec_value':
                    new_ser_par.spec_value = item[1]
            session.add(new_ser_par)

    if data.get('changed_entries'):
        for entry in data.get('changed_entries'):
            ser_par = ServiceParams.query.get(str(entry.get('offer_id')))
            if not ser_par:
                return jsonify({
                    'text': 'Ошибка при редактировании одной из записей (не найден идентификатор)'
                }), 404
            for item in entry.items():
                if item[0] == 'parent':
                    if not item[1]:
                        ser_par.parent_id = None
                    else:
                        param = ServiceParams.query.get(str(item[1]))
                        if param:
                            ser_par.parent = param
                if item[0] == 'name':
                    ser_par.name = item[1]
                if item[0] == 'u_name':
                    ser_par.u_name = item[1]
                if item[0] == 'spec_value':
                    ser_par.spec_value = item[1]

    if data.get('deprecated_entries'):
        for entry in data.get('deprecated_entries'):
            ser_par = ServiceParams.query.get(str(entry.get('offer_id')))
            if not ser_par:
                return jsonify({
                    'text': 'Ошибка при редактировании одной из записей (не найден идентификатор)'
                }), 404
            ser_par.deprecated = True

    if data.get('respawn_entries'):
        for entry in data.get('respawn_entries'):
            ser_par = ServiceParams.query.get(str(entry.get('offer_id')))
            if not ser_par:
                return jsonify({
                    'text': 'Ошибка при редактировании одной из записей (не найден идентификатор)'
                }), 404
            ser_par.deprecated = False

    if data.get('purge_entries'):
        for entry in data.get('purge_entries'):
            ser_par = ServiceParams.query.get(str(entry.get('offer_id')))
            if not ser_par:
                return jsonify({
                    'text': 'Ошибка при удалении одной из записей (не найден идентификатор)'
                }), 404

            session.delete(ser_par)

    try:
        session.commit()
    except exc.IntegrityError:
        return jsonify({
            'text': 'Один из выбранных элементов не может быть удален тк уже используеться (можете воспользоваться пунктом УСТАРЕЛО)'
        }), 403

    return jsonify({})