# from flask import render_template, jsonify
# from flask_login import login_required
# from webargs.flaskparser import use_args
# from sqlalchemy.orm import aliased

# from src.schemas.administration import phone_repair_updates_post
# from src.db import session
# from src.db.models import ServiceParams, ServicePhoneRepair, CrossTradeinOrders
# from src.lib.access import allow_view
# from . import bp_admin

# @bp_admin.route('/phone_repair/<service>')
# @login_required
# @allow_view(["admin"])
# def phone_repair(service):
#     SPModel = aliased(ServiceParams)
#     service = ServiceParams.get_by_uname(service)
#     offers = ServicePhoneRepair.query.filter_by(service_id=service.id).join(SPModel, ServicePhoneRepair.model).order_by(SPModel.name.desc()).all()

#     offers_list = dict()
#     if offers:
#         offers_list = [{
#             'id': offer.id,
#             'phone_repair_model': offer.model.u_name,
#             'price1': offer.price1,
#             'price2': offer.price2,
#             'sale': offer.sale,
#             'deprecated': offer.deprecated,
#         } for offer in offers]

#     params = dict()
#     for name_param in ['models_iphones']:
#         service_params = ServiceParams.query.filter(ServiceParams.parent.has(u_name=str(name_param))).all()
#         name_param_vals = []
#         for service_param in service_params:
#             if not service_param.deprecated:
#                 name_param_vals.append({
#                     'name': service_param.name,
#                     'val': service_param.u_name
#                 })
#         if name_param_vals:
#             params.update({name_param: name_param_vals})
#     params.update({
#         'service': service.u_name,
#         'service_name': service.name,
#         'service_id': service.id
#         })
#     # print(params)
#     return render_template('admin_panel/phone_repair.html', params=params, offers_list=offers_list)


# @bp_admin.route('/phone_repair/updates', methods=['POST'])
# @login_required
# @allow_view(["admin"])
# @use_args(phone_repair_updates_post)
# def phone_repair_updates(data):
#     if not data.get('new_entries') and not data.get('changed_entries') and not data.get('deprecated_entries') and not data.get('respawn_entries') and not data.get('purge_entries'):
#         return jsonify({
#             'text': 'Изменения отсутствуют'
#         }), 422

#     if data.get('new_entries'):
#         for entry in data.get('new_entries'):
#             new_offer = ServicePhoneRepair()
#             for item in entry.items():
#                 if item[0] == 'phone_repair':
#                     param = ServiceParams.get_by_uname(item[1], group='models_iphones')
#                     if param:
#                         new_offer.model = param
#                 if item[0] == 'price1':
#                     new_offer.price1 = item[1]
#                 if item[0] == 'service_id':
#                     new_offer.service_id = str(item[1])
#                 if item[0] == 'price2':
#                     new_offer.price2 = item[1]
#                 if item[0] == 'sale':
#                     new_offer.sale = item[1]
#             session.add(new_offer)

#     if data.get('changed_entries'):
#         for entry in data.get('changed_entries'):
#             offer = ServicePhoneRepair.query.get(str(entry.get('offer_id')))
#             if not offer:
#                 return jsonify({
#                     'text': 'Ошибка при редактировании одной из записей (не найден идентификатор)'
#                 }), 404
#             for item in entry.items():
#                 if item[0] == 'phone_repair':
#                     param = ServiceParams.get_by_uname(item[1], group='models_iphones')
#                     if param:
#                         offer.model = param
#                 if item[0] == 'price1':
#                     offer.price1 = item[1]
#                 if item[0] == 'price2':
#                     offer.price2 = item[1]
#                 if item[0] == 'sale':
#                     offer.sale = item[1]

#     if data.get('deprecated_entries'):
#         for entry in data.get('deprecated_entries'):
#             offer = ServicePhoneRepair.query.get(str(entry.get('offer_id')))
#             if not offer:
#                 return jsonify({
#                     'text': 'Ошибка при редактировании одной из записей (не найден идентификатор)'
#                 }), 404
#             offer.deprecated = True

#     if data.get('respawn_entries'):
#         for entry in data.get('respawn_entries'):
#             offer = ServicePhoneRepair.query.get(str(entry.get('offer_id')))
#             if not offer:
#                 return jsonify({
#                     'text': 'Ошибка при редактировании одной из записей (не найден идентификатор)'
#                 }), 404
#             offer.deprecated = False

#     if data.get('purge_entries'):
#         for entry in data.get('purge_entries'):
#             offer = ServicePhoneRepair.query.get(str(entry.get('offer_id')))
#             if not offer:
#                 return jsonify({
#                     'text': 'Ошибка при удалении одной из записей (не найден идентификатор)'
#                 }), 404
#             orders = CrossTradeinOrders.query.filter_by(old_device_id=str(entry.get('offer_id'))).first()
#             if orders:
#                 return jsonify({
#                     'text': 'Один из выбранных элементов не может быть удален тк уже используеться (можете воспользоваться пунктом УСТАРЕЛО)'
#                 }), 403

#             session.delete(offer)

#     session.commit()

#     return jsonify({})