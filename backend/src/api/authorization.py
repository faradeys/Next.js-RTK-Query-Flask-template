"""login API."""
import random, string
from flask import current_app, request, g
from flask_restful import Resource
from webargs.flaskparser import use_args
from xml.etree import ElementTree
import requests

from src.db import db, session
from src.db.models import User, Role
from src.schemas.authorization import login_post, reg_post, restore_pass_post
from src.lib.access import allow, revoke_token, auth_greenlight, reset_pass_greenlight
from src.lib.sending import send_sms
from src.lib.utils import parse_phone


class LoginAPI(Resource):
    @use_args(login_post)
    @auth_greenlight
    def post(self, data):
        user = User.query.filter( db.or_(User.roles.any(name='user')) ).filter_by(phone=parse_phone(data.get('phone')), is_verified=True, is_deleted=False).first()

        if not user:
            return {
                "message": "not authorized"
            }, 401

        if user.is_banned:
            return {
                "message": "user is banned"
            }, 423

        if not user.verify_password(data.get('password')):
            return {
                "message": "not authorized"
            }, 401

        return {
            'access_token':  user.generate_auth_token()
        }


class LogoutAPI(Resource):
    @allow(["all"])
    def post(self):
        revoke_token(g.current_user.id)

        return {
            "message": "OK"
        }


class RegistrationAPI(Resource):
    @use_args(reg_post)
    def post(self, data):
        parsed_phone = parse_phone(data.get('phone'))
        user = User.check_phone_number(parsed_phone)

        if user and user.is_verified:
            if user.is_banned:
                return {
                    "message": "user is banned"
                }, 423

            return {
                "message": "user with this phone number already exist"
            }, 409

        if not user:
            user = User.new_one(parsed_phone)

        if data.get('name'):
            user.name = data.get('name')

        user.hash_password(data.get('password'))
        user.is_verified = True

        session.commit()

        return {
            "uid": user.id
        }



class RestorePassAPI(Resource):
    @use_args(restore_pass_post)
    @reset_pass_greenlight
    def post(self, data):
        if not data.get('phone'):
            return {
                "message": "need a phone"
            }, 422

        if not data.get('token'):
            return {
                "message": "need a token"
            }, 422

        not_a_bot = False

        if data.get('token'):
            secret = current_app.config['RECAPTCHA_SECRET']
            token = data.get('token')
            url = 'https://www.google.com/recaptcha/api/siteverify?secret={}&response={}'.format(secret, token)

            response = requests.post(
                url,
            )
            response_dict = response.json()

            if response_dict['success'] == True:
                not_a_bot = True
            else:
                return {
                    "message": "need a token"
                }, 400

        if not_a_bot:
            user = User.check_phone_number(parse_phone(data.get('phone')), verified=True)

            if not user:
                return {
                    "message": "user not found"
                }, 404

            if user.is_banned:
                return {
                    "message": "user is banned"
                }, 423

            new_passw = user.hash_password()
            sms_text = 'Ваш новый пароль от ЛК: '+new_passw

            if not send_sms(sms_text, user.phone):
                return {
                    "message": "auth sms message not delivered"
                }, 400

            session.commit()

            return {
                "message": "OK"
            }
