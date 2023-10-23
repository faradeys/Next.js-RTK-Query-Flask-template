# import re
# from flask import request, g
# from flask_restful import Resource
# from webargs.flaskparser import use_args

# from src.db import session, db
# from src.db.models import Orders, ReferalCode
# from src.lib.access import allow, validate_uuid


# class OrdersListAPI(Resource):
#     @allow(['user'])
#     def get(self):
#         orders = list()
#         orders.extend(Orders.get_all())
#         orders.extend(CrossTradeinOrders.get_all())

#         if not orders:
#             return {}

#         orders_list = list()
#         for order in orders:
#             if order.order_info:

#                 order_info = {
#                     'id': order.id,
#                     'nice_id': str(order.id)[0:7].upper(),
#                     'order_type': order.order_type,
#                     'old_device': None,
#                     'old_device_model': None,
#                     'old_device_type': None,
#                     'old_device_type_name': None,
#                     'old_device_price': None,
#                     'new_device': None,
#                     'new_device_model': None,
#                     'new_device_price': None,
#                     'new_device_type': None,
#                     'new_device_type_name': None,
#                     'sell_only': order.sell_only if hasattr(order, 'sell_only') else None,
#                     'created_at': order.created_at.isoformat() if order.created_at else "",
#                     'referal_code': None
#                 }
#                 if hasattr(order, 'old_device_sell_type'):
#                     if order.old_device_sell_type:
#                         order_info.update({
#                             'old_device_type': order.old_device_sell_type.u_name,
#                             'old_device_type_name': order.old_device_sell_type.name,
#                             'old_device': order.order_info['sell_device']['params']['model'][1],
#                             'old_device_model': order.old_device.model.u_name if order.old_device.model else '',
#                             'old_device_price': order.order_info['sell_device']['price']
#                         })
#                 if hasattr(order, 'new_device_sell_type'):
#                     if order.new_device_sell_type:
#                         order_info.update({
#                             'new_device_type': order.new_device_sell_type.u_name,
#                             'new_device_type_name': order.new_device_sell_type.name,
#                             'new_device': order.order_info['new_device']['params']['model'][1],
#                             'new_device_model': order.new_device.model.u_name,
#                             'new_device_price': order.order_info['new_device']['price']
#                         })
#                 if hasattr(order, 'referrer'):
#                     if order.referrer:
#                         order_info.update({
#                             'referal_code': order.referrer.code
#                         })
#                 if hasattr(order, 'referal_code'):
#                     order_info.update({
#                         'referal_code': order.referal_code
#                     })
#                 orders_list.append(order_info)

#         orders_list.sort(key=lambda x: x['created_at'], reverse=True)
#         return orders_list


# class OrderInfo(Resource):
#     def get(self, id):
#         if not validate_uuid(id):
#             return {
#                "message": "no such order",
#             }, 404
#         order = CrossTradeinOrders.query.filter_by(id=id).first()
#         if not order:
#             return {
#                 "message": "no such order"
#             }, 404

#         order_info = {
#             'id': order.id,
#             'nice_id': str(order.id)[0:7].upper(),
#             'order_data': order.save_order_info,
#             'created_at': order.created_at.isoformat() if order.created_at else "",
#         }
#         return order_info
