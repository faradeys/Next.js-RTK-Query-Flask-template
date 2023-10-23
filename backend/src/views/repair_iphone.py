from flask import render_template, jsonify
from flask_login import login_required
from webargs.flaskparser import use_args
from sqlalchemy.orm import aliased

from src.lib.access import allow_view
from src.db import session
from src.db.models import ServiceParams, Prices, Orders
from . import bp_admin
from src.schemas.administration import iphone_repair_updates_post

@bp_admin.route('/repair_iphone')
@login_required
@allow_view(["admin"])
def repair_iphone():
    SPModel = aliased(ServiceParams)
    SPService = aliased(ServiceParams)
    SPProblem = aliased(ServiceParams)
    offers = Prices.query.join(SPModel, Prices.model).join(SPService, Prices.service).join(SPProblem, Prices.problem).order_by(Prices.deprecated.asc(), SPModel.name.desc(), SPService.name.asc(), Prices.created_at.desc()).all()
    offers_list = list()
    
    if offers:
        offers_list = [{
            'id': offer.id,
            'model': offer.model.name,
            'service_id': offer.service_id,
            'service': offer.service.name,
            'service_val': offer.service.u_name,
            'problem': offer.problem.name,
            'problem_val': offer.problem.u_name,
            'price': offer.price
        } for offer in offers]

    params = dict()
    for name_param in ['models_iphone', 'broken_part_iphone']:
        service_params = ServiceParams.query.filter(ServiceParams.parent.has(u_name=str(name_param))).all()
        if service_params:
            name_param_vals = []
            for service_param in service_params:
                if not service_param.deprecated:
                    name_param_vals.append({
                        'name': service_param.name,
                        'val': service_param.u_name
                    })
            if name_param_vals:
                params.update({
                    name_param: name_param_vals
                })

    problem_params_dict = dict()
    parents_problem_params = ServiceParams.query.filter(ServiceParams.parent.has(u_name='broken_part_iphone')).all()
    if parents_problem_params:
        for parents_problem_param in parents_problem_params:
            problem_params = ServiceParams.query.filter(ServiceParams.parent.has(id=parents_problem_param.id)).all()
            if problem_params:
                name_param_vals = []
                for problem_param in problem_params:
                    if not problem_param.deprecated:
                        name_param_vals.append({
                            'parent_id': parents_problem_param.id,
                            'name': problem_param.name,
                            'val': problem_param.u_name
                        })
                if name_param_vals:
                    problem_params_dict.update({
                        parents_problem_param.u_name: name_param_vals
                    })

    return render_template('admin_panel/repair_iphone.html', params=params, offers_list=offers_list, problem_params=problem_params_dict)

@bp_admin.route('/repair_iphone/updates', methods=['POST'])
@login_required
@allow_view(["admin"])
@use_args(iphone_repair_updates_post)
def phone_repair_updates(data):
    if not data.get('new_entries') and not data.get('changed_entries') and not data.get('deprecated_entries') and not data.get('respawn_entries') and not data.get('purge_entries'):
        return jsonify({
            'text': 'Изменения отсутствуют'
        }), 422

    if data.get('new_entries'):
        for entry in data.get('new_entries'):
            new_offer = Prices()

            for item in entry.items():
                if item[0] == 'price':
                    new_offer.price = item[1]
                if item[0] == 'broken_part':
                    param = ServiceParams.get_by_uname(item[1], )
                    if param:
                        new_offer.service = param
                if item[0] == 'models_iphones':
                    param = ServiceParams.get_by_uname(item[1], )
                    if param:
                        new_offer.model = param
                if item[0] == 'problem':
                    param = ServiceParams.get_by_uname(item[1], )
                    if param:
                        new_offer.problem = param

            session.add(new_offer)

    if data.get('changed_entries'):
        for entry in data.get('changed_entries'):
            offer = Prices.query.get(str(entry.get('offer_id')))
            if not offer:
                return jsonify({
                    'text': 'Ошибка при редактировании одной из записей (не найден идентификатор)'
                }), 404
            
            for item in entry.items():
                if item[0] == 'price':
                    offer.price = item[1]
                if item[0] == 'broken_part':
                    param = ServiceParams.get_by_uname(item[1], )
                    if param:
                        offer.service = param
                if item[0] == 'models_iphones':
                    param = ServiceParams.get_by_uname(item[1], )
                    if param:
                        offer.model = param
                if item[0] == 'problem':
                    param = ServiceParams.get_by_uname(item[1], )
                    if param:
                        offer.problem = param

    if data.get('deprecated_entries'):
        for entry in data.get('deprecated_entries'):
            offer = Prices.query.get(str(entry.get('offer_id')))
            if not offer:
                return jsonify({
                    'text': 'Ошибка при редактировании одной из записей (не найден идентификатор)'
                }), 404
            offer.deprecated = True

    if data.get('respawn_entries'):
        for entry in data.get('respawn_entries'):
            offer = Prices.query.get(str(entry.get('offer_id')))
            if not offer:
                return jsonify({
                    'text': 'Ошибка при редактировании одной из записей (не найден идентификатор)'
                }), 404
            offer.deprecated = False

    if data.get('purge_entries'):
        for entry in data.get('purge_entries'):
            offer = Prices.query.get(str(entry.get('offer_id')))
            
            if not offer:
                return jsonify({
                    'text': 'Ошибка при удалении одной из записей (не найден идентификатор)'
                }), 404
            orders = Orders.query.filter_by(ordered_service_id=str(entry.get('offer_id'))).first()
            if orders:
                return jsonify({
                    'text': 'Один из выбранных элементов не может быть удален тк уже используеться (можете воспользоваться пунктом УСТАРЕЛО)'
                }), 403

            session.delete(offer)

    session.commit()
    return jsonify({})
