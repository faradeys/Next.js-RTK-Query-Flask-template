"""Initialization API."""
from flask import Blueprint, request, g
from flask_restful import Api

from src.db.models import User
from src.api import (
    ping,
    authorization,
    me,
    media,
    service,
    user_service_state,
    side_authorization,
    referal_codes,
    user_text_store,
    orders,
    promo_codes,
)

bp_app = Blueprint('bp_app', __name__)
api = Api(bp_app)

@bp_app.before_request
def current_user():
    """get current user by token"""

    req_token = request.headers.get('Authorization')
    _current_user = User()
    if req_token:
        user = User.verify_auth_token(req_token)
        if user:
            _current_user = user
    with request:
        g.current_user = _current_user
        g.user_ip = request.remote_addr
        g.host = request.headers.get('Host')

#user authorization
api.add_resource(ping.PingAPI, '/ping')
api.add_resource(authorization.LoginAPI, '/login')
api.add_resource(authorization.LogoutAPI, '/logout')
api.add_resource(authorization.RegistrationAPI, '/reg')
api.add_resource(authorization.RestorePassAPI, '/restore_pass')
api.add_resource(side_authorization.VKSideAuthAPI, '/login/vk')
api.add_resource(side_authorization.FBSideAuthAPI, '/login/fb')

#user data
api.add_resource(me.MeAPI, '/me')
api.add_resource(me.MePhoneUpdateAPI, '/me/change_phone')
api.add_resource(me.MePassUpdateAPI, '/me/change_pass')
api.add_resource(me.MeMailUpdateAPI, '/me/change_email')

# api.add_resource(orders.OrdersListAPI, '/orders')
# api.add_resource(orders.OrderInfo, '/order/<id>')

#iphone repair services
api.add_resource(service.ServiceAPI, '/service/params')
api.add_resource(service.ServiceOrderAPI, '/service/send')
# api.add_resource(prices.ServicePhoneRepairOrdersListAPI, '/orders/phone_repair')
# api.add_resource(prices.ServicePhoneRepairOrderDataAPI, '/orders/phone_repair/<order_id>')
# api.add_resource(prices.ServicePhoneRepairAPI, '/phone_repair')

#user_text
api.add_resource(user_text_store.GetUserTextsAPI, '/user_text')
api.add_resource(user_text_store.SetUserTextAPI, '/user_text/send')

#referal
api.add_resource(referal_codes.CheckReferalCodeAPI, '/referal')
api.add_resource(referal_codes.InviteFriendAPI, '/invite_friend')

#promo-codes
api.add_resource(promo_codes.CheckPromoCodeAPI, '/promo/check')

#file upload
api.add_resource(media.FileUploadAPI, '/upload')
api.add_resource(media.FileUploadAPI, '/upload/<string:uid>', endpoint='upload_by_id', methods=['GET'])

#user service state
api.add_resource(user_service_state.UserServiceStateAPI, '/service_state/save')
api.add_resource(user_service_state.UserServiceStateAPI, '/service_state/<string:state_id>', endpoint='user_service_state_by_id', methods=['GET'])
