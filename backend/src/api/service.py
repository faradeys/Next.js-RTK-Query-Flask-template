from flask import request, g
from flask_restful import Resource
from webargs.flaskparser import use_args

from src.db import session, db
from src.db.models import User, ServiceParams, Prices, Orders
from src.lib.access import allow, validate_uuid
from src.lib.sending import order_notification, sms_order_notify
from src.lib.utils import parse_phone
from src.schemas.repair_data import repair_order_post


class ServiceAPI(Resource):
    def get(self):
        filters = {'deprecated': False}
        offers_params = Prices.query.filter_by(**filters).all()

        if offers_params:
            resp = dict()

            for offer_params in offers_params:
                model = offer_params.model.u_name

                if not model in resp.keys():
                    resp.update({
                        offer_params.model.u_name: {
                            'id': offer_params.model.id,
                            'abbr': offer_params.model.u_name,
                            'name': offer_params.model.name,
                            'specValue': int(offer_params.model.spec_value) if offer_params.model.spec_value else 0,
                            'damages': dict()
                        }
                    })

                if not offer_params.service.u_name in resp[offer_params.model.u_name]['damages'].keys():
                    resp[offer_params.model.u_name]['damages'].update({
                        offer_params.service.u_name: {
                            'id': offer_params.service.id,
                            'name': offer_params.service.name,
                            'abbr': offer_params.service.u_name,
                            'specValue': int(offer_params.service.spec_value) if offer_params.service.spec_value else 0,
                            'problems': dict()
                        }
                    })

                if not offer_params.problem.u_name in resp[offer_params.model.u_name]['damages'][offer_params.service.u_name]['problems'].keys():
                    resp[offer_params.model.u_name]['damages'][offer_params.service.u_name]['problems'].update({
                        offer_params.problem.u_name: {
                            'id': offer_params.problem.id,
                            'name': offer_params.problem.name,
                            'abbr': offer_params.problem.u_name,
                            'specValue': int(offer_params.problem.spec_value) if offer_params.problem.spec_value else 0,
                            'priceId': offer_params.id,
                            'price': offer_params.price
                        }
                    })
        return resp


class ServiceOrderAPI(Resource):
    @use_args(repair_order_post)
    def post(self, data):
        phone = data.get('phone')
        model_id = data.get('model')
        problems = data.get('problems')
        damages = data.get('damages')
        service_type = data.get('serviceType')
        type_connection = data.get('typeConnection') or ''
        name = data.get('name') or ''

        if not phone or not model_id or not problems or not damages or not service_type:
            return {
                "message": "{INVALID_DATA}"
            }, 403

        user = User.check_phone_number(phone)
        is_new_user = False

        if not user:
            is_new_user = True
            user = User.new_one(phone)
            user.name = name
        if not user.is_verified:
            user.is_verified = True

        if user.is_banned:
            return {
                "message": "user is banned"
            }, 423

        model = ServiceParams.query.filter_by(id=model_id).first()
        service_type = ServiceParams.get_by_uname(service_type)
        union_list = list()
        problems_list_order = list()
        damages_list_order = list()
        final_price = 0

        for damage in damages:
            damage_params = ServiceParams.query.filter_by(
                id=damage).first()
            problems_list = list()
            damages_list_order.append(damage_params.name)
            if damage_params:
                for problem in problems:
                    problem_params = ServiceParams.query.filter_by(
                        id=problem).first()
                    if problem_params:
                        if problem_params.parent.name == damage_params.name:
                            ordered_problem = Prices.query.filter_by(
                                problem_id=problem).first()
                            problems_list.append(problem_params.name)
                            problems_list_order.append(problem_params.name)
                            final_price += ordered_problem.price

            union_list.append({
                damage_params.name: problems_list
            })

        order = Orders()
        order.customer = user
        order.name = name
        order.phone = phone
        order.price = final_price
        order.ordered_damages = ', '.join(damages_list_order)
        order.ordered_problems = ','.join(problems_list_order)
        order.model_id = model.id
        session.add(order)
        session.commit()

        new_user_passw = user.hash_password() if is_new_user else None
        sms_order_notify(user.phone, new_user_passw)
        session.commit()

        msg = "<b>Новый заказ на ремонт {service_type}</b>\r\n\r\n"\
            "Модель: {model}\r\n" \
            "Проблемы: {ordered_problems}\r\n"\
            "Что сломалось: {ordered_damages}\r\n"\
            "Цена: {price}\r\n"\
            "Имя клиента: {name}\r\n"\
            "Номер телефона: {phone}\r\n" \
            "Удобный тип связи: {type_connection} \r\n" \
            .format(**dict(
                model=order.order_info['model'],
                ordered_problems=order.order_info['problems'],
                ordered_damages=order.order_info['damages'],
                price=order.order_info['price'],
                name=order.order_info['name'],
                phone=phone,
                service_type=service_type.name,
                type_connection=type_connection
            ))

        order_notification(msg)

        return {
            "orderId": order.id
        }
# class ServicePhoneRepairOrderAPI(Resource):
#     @use_args(service_phone_repair_orders_post)
#     def post(self, data):
#         parsed_phone = parse_phone(data.get('phone'))
#         user = User.check_phone_number(parsed_phone)
#         is_anon = False
#         if not user:
#             is_anon = True
#             user = User.new_one(parsed_phone)
#             user.name = data.get('name')
#         if not user.is_verified:
#             user.is_verified = True

#         if user.is_banned:
#             return {
#                 "message": "user is banned"
#             }, 423

#         model = ServiceParams.get_by_uname(data.get('model'), group='models_iphones')
#         service = ServiceParams.get_by_uname(data.get('defect_type'))
#         if model and service:
#             ordered_service = ServicePhoneRepair.query.filter_by(
#                 model_id=model.id,
#                 service_id=service.id,
#                 deprecated=False
#             ).first()

#             if ordered_service:
#                 order = ServicePhoneRepairOrders()
#                 order.customer = user
#                 order.name = data.get('name')
#                 order.phone = parsed_phone
#                 order.sale = data.get('sale')
#                 order.city = data.get('city')
#                 order.color = data.get('color')
#                 order.selected_price_type = data.get('price_type')
#                 order.ordered_service = ordered_service
#                 session.add(order)
#                 session.commit()

#                 new_user_passw = user.hash_password() if is_anon else None
#                 sms_order_notify(user.phone, new_user_passw)
#                 session.commit()

#                 when_time = ''
#                 meet_time = ''
#                 if order.order_info:
#                     if data.get('meet_time'):
#                         meet_time = data.get('meet_time')
#                     if data.get('when_time'):
#                         when_time = data.get('when_time')

#                     msg = "<b>Новый заказ '{service_type}'</b>\r\nМодель: {model}\r\nЦвет: {color}\r\nСкидка: {sale}\r\nЦена заказа: {selected_price}\r\nТип: {selected_type}\r\nИмя клиента: {name}\r\nНомер телефона: {phone}\r\nГород: {city}\r\nДень: {when}\r\nВремя: {meet_time}".format(**dict(
#                         service_type = order.order_info['service_type'],
#                         model = order.order_info['model'],
#                         color = order.order_info['color'],
#                         sale = 'Да' if order.order_info['sale'] else 'Нет',
#                         selected_price = order.order_info['selected_price'],
#                         selected_type = 'оригинал' if data.get('price_type') == 'counted_price' else 'китай',
#                         name = order.order_info['name'],
#                         phone = parsed_phone,
#                         city = order.order_info['city'],
#                         when = when_time,
#                         meet_time = meet_time,
#                     ))

#                     if(service.u_name == 'service_display'):
#                         msg += "\r\nЗащитное стекло: {glass}".format(**dict(
#                             glass = data.get('glass')
#                         ))

#                     order_notification(msg)
#                 return {}
#         return {
#             "message": "Cant find service by requested criteria"
#         }, 404

# class ServicePhoneRepairParamsAPI(Resource):
#     def post(self):
#         filters = {'deprecated': False}
#         offers_params = ServicePhoneRepair.query.filter_by(**filters).all()

#         colors = DeviceColors.get('models_iphones', type='params')

#         if offers_params:
#             resp = dict()
#             for offer_params in offers_params:
#                 model = offer_params.model.u_name
#                 if not model in resp.keys():
#                     colors_dict = {}
#                     if model in colors.keys():
#                         colors_dict = {
#                             'group_name': colors['group_name'],
#                             'group_abbr': colors['group_abbr'],
#                             'vals': colors[model]
#                         }
#                     resp.update({
#                         model: {
#                             'device_abbr': model,
#                             'device_name': offer_params.model.name,
#                             'seq_position': int(offer_params.model.spec_value) if offer_params.model.spec_value else 0,
#                             'params': {
#                                 colors['group_abbr']: colors_dict
#                             },
#                         }
#                     })

#             return sorted(resp.values(), key=lambda k: k['seq_position'], reverse=True)

#         return {}

# class ServicePhoneRepairOrdersListAPI(Resource):
#     @allow(['user'])
#     def get(self):
#         orders = ServicePhoneRepairOrders.get_all()

#         orders_list = list()
#         if not orders:
#             return {}

#         for order in orders:
#             order_info = {
#                 'id': order.id,
#                 'nice_id': str(order.id)[0:7].upper(),
#                 'created_at': order.created_at.isoformat()if order.created_at else "",
#             }

#             orders_list.append(order_info)

#         return orders_list


# class ServicePhoneRepairOrderDataAPI(Resource):
#     @allow(['user'])
#     def get(self, order_id):
#         if not validate_uuid(order_id):
#             return {
#                "message": "no such order",
#             }, 404

#         order = ServicePhoneRepairOrders.get_one_own(order_id)
#         if not order:
#             return {
#                 "message": "no such order"
#             }, 404

#         return {
#             'id': order.id,
#             'nice_id': str(order.id)[0:7].upper(),
#             'created_at': order.created_at.isoformat() if order.created_at else '-',
#             'order_data': order.order_info
#         }


# class ServicePhoneRepairAPI(Resource):
#     @use_args(service_phone_repair_post)
#     def post(self, data):
#         model = ServiceParams.get_by_uname(data.get('model'), group='models_iphones')
#         service = ServiceParams.get_by_uname(data.get('defect_type'))
#         if isinstance(model, ServiceParams) and isinstance(service, ServiceParams):
#             prices = ServicePhoneRepair.query.filter_by(
#                 model_id=model.id,
#                 service_id=service.id,
#                 deprecated=False
#             ).first()

#             if prices:
#                 return prices.ger_prices_dict
#         return {
#             "message": "Cant find service by requested criteria"
#         }, 404
