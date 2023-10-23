from flask_restful import Resource
from webargs.flaskparser import use_args

from src.db import session, db
from src.db.models import ReferalCode, User
from src.schemas.referal_codes import check_referal_code_post, invite_friend_post
from src.lib.sending import send_sms
from src.lib.utils import parse_phone
from src.lib.access import invite_friend_greenlight


class CheckReferalCodeAPI(Resource):
    @use_args(check_referal_code_post)
    def post(self, data):
        referrer = ReferalCode.find(data.get('referal_code'))
        if not referrer:
            return {
                "message": "not valid referal code"
            }, 404

        if referrer.service_type:
            return {
                "service_type": referrer.service_type.u_name
            }


class InviteFriendAPI(Resource):
    @use_args(invite_friend_post)
    @invite_friend_greenlight
    def post(self, data):
        referrer = ReferalCode.find(data.get('referal_code'))
        if not referrer:
            return {
                "message": "not valid referal code"
            }, 404

        phone_number = parse_phone(data.get('phone'))
        user = User.check_phone_number(phone_number)
        if user:
            return {
                "message": "user already exist"
            }, 409

        device_services = {
            'ipad_buyout': 'iPad',
            'ipad_tradein': 'iPad',
            'samsung_buyout': 'Samsung',
            'samsung_tradein': 'Samsung',
            'iphone_buyout': 'iPhone',
            'iphone_tradein': 'iPhone',
            'macbook_buyout': 'MacBook',
            'macbook_tradein': 'MacBook'
        }

        if not send_sms('Продаешь '+(device_services[referrer.service_type.u_name] if referrer.service_type.u_name in device_services else 'iPhone')+'? Купим дорого. Твой друг рекомендует 👍 https://damprodam.ru/invite/'+referrer.code, phone_number):
            return {
                "message": "auth sms message not delivered"
            }, 400

        referrer.invite_by_sms = True
        User.new_one(phone_number, verified=False)
        session.commit()

        return {}
