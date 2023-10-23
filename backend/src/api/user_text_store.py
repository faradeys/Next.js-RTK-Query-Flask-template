import requests

from flask_restful import Resource
from webargs.flaskparser import use_args
from urllib.parse import unquote
from flask import current_app

from src.db import session, db
from src.db.models import UserTextStore
from src.schemas.user_text_store import get_users_texts, set_user_text_post
from src.lib.access import allow
from src.lib.utils import parse_phone
from src.lib.sending import order_notification


class GetUserTextsAPI(Resource):
    @allow(["admin"])
    @use_args(get_users_texts)
    def post(self, data):
        parsed_phone = parse_phone(data.get('phone')) if data.get('phone') else ""
        if not parsed_phone:
            return {
                "message": "no such entry"
            }, 404

        user_texts = UserTextStore.query.filter_by(phone=parsed_phone).all()
        if not user_texts:
            return {
                "message": "no such entry"
            }, 404

        parsed_user_texts = list()
        for user_data in user_texts:
            parsed_user_texts.append({
                'name': user_data.name,
                'email': user_data.email,
                'text': user_data.text,
            })

        return {
            'phone': user_texts[0].phone,
            'texts': parsed_user_texts,
        }



class SetUserTextAPI(Resource):
    @use_args(set_user_text_post)
    def post(self, data):
        if not data.get('phone') and not data.get('name') and not data.get('text') and not data.get('email'):
            return {
                "message": "need at least phone or name or text or email"
            }, 422

        if not data.get('token'):
            return {
                "message": "need a token"
            }, 422
        
        not_a_bot = False

        if data.get('from') and data.get('from') == 'telegram':
            not_a_bot = True
        
        if data.get('token') and not data.get('from'):
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
            parsed_phone = parse_phone(data.get('phone')) if data.get('phone') else ""

            user_text = UserTextStore(
                name=data.get("name"),
                email=data.get("email"),
                text=data.get("text"),
                phone=parsed_phone
            )

            if data.get('utm'):
                user_text.utm = data.get('utm')

            session.add(user_text)
            session.commit()

            title = data.get('title') if data.get('title') else "Новое сообщение пользователя"

            msg = "<b>{title}</b>\r\n\r\n" \
                "- Имя: {name}\r\n" \
                "- Телефон: {phone}\r\n\r\n" \
                .format(**dict(
                title=title,
                name=user_text.name,
                phone='+' + user_text.phone[0]+' ('+user_text.phone[1:4]+') '+user_text.phone[4:7]+'-'+user_text.phone[7:]
            ))

            if user_text.email:
                msg += "Email: {email}\r\n\r\n" \
                .format(**dict(
                    email=unquote(user_text.email)
                ))
            
            if user_text.text:
                msg += "{text}\r\n\r\n" \
                .format(**dict(
                    text=unquote(user_text.text)
                ))
            
            if user_text.utm:
                msg += "utm: {utm}\r\n" \
                .format(**dict(
                    utm=unquote(user_text.utm)
                ))
            
            message_id = order_notification(msg)
            user_text.message_id = message_id
            session.commit()

            return {
                "id": str(user_text.id)[0:7]
            }
