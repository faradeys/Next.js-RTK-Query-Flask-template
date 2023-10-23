from flask import request, g
from flask_restful import Resource
from webargs.flaskparser import use_args

from src.db import session, db
from src.db.models import User, File
from src.lib.access import allow, generate_phone_change_code, verify_phone_change_code, verify_mail_change_code
from src.schemas.user import me_patch, me_phone_update_post, me_pass_update_post, me_mail_update_post
from src.lib.sending import send_sms, send_email, send_verify_email_code
from src.lib.utils import parse_phone



class MeAPI(Resource):
    @allow(["user"])
    def get(self):
        return {
            'id': g.current_user.id,
            'is_side_auth': True if g.current_user.side_id else False,
            'name': g.current_user.name,
            'email': g.current_user.email,
            'city': g.current_user.city,
            'phone': g.current_user.phone,
            'bonuses': g.current_user.bonuses,
            'created_at': g.current_user.created_at.isoformat(),
            'avatar_id': g.current_user.avatar_id,
            'avatar_path': g.current_user.avatar_path,
            'referal_code': g.current_user.referal_code,
        }

    @allow(["all"])
    @use_args(me_patch)
    def patch(self, data):
        if not data:
            return {
                "message": "no data"
            }, 422

        for check in me_patch:
            if data.get(check):
                if check == 'avatar_id':
                    avatar_to_attach = File.query.get(str(data.get(check)))
                    if not avatar_to_attach:
                        return {
                            "message": "no such file",
                        }, 400
                    if not avatar_to_attach.file_mimetype[:6] == 'image/':
                        return {
                            "message": "{} incorrect mimetype for user avatar ".format(avatar_to_attach.file_mimetype),
                        }, 400

                setattr(g.current_user, check, data.get(check))

        session.commit()

        return {}


class MePhoneUpdateAPI(Resource):
    @allow(["user"])
    @use_args(me_phone_update_post)
    def post(self, data):
        if data.get('phone'):
            verify_code = generate_phone_change_code(parse_phone(data.get('phone')))
            if not verify_code:
                return {
                    "message": "sms send code cooldown"
                }, 403

            sms_resp = send_sms('Проверочный код: ' + str(verify_code), data.get('phone'))
            if not sms_resp:
                return {
                    "message": "sms message not delivered"
                }, 400

            return {}

        if data.get('verify_code'):
            new_phone = verify_phone_change_code(data.get('verify_code'))
            if not new_phone:
                return {
                    "message": "invalid code"
                }, 403

            same_phone_user = User.query.filter(db.or_(User.roles.any(name='user'))).filter_by(phone=parse_phone(new_phone), is_verified=True, is_deleted=False, is_banned=False).first()
            if same_phone_user:
                same_phone_user.is_deleted = True
                same_phone_user.deleted_at = db.text('now()::timestamp(0)')
                g.current_user.bonus_top_up(same_phone_user.bonuses)

            g.current_user.phone = new_phone

            if not g.current_user.password:
                new_pass = g.current_user.hash_password()
                if new_pass:
                    send_sms('Теперь вы также можете авторизоваться по номеру телефона с этим паролем: '+new_pass, new_phone)

            session.commit()

            return {}

        return {
            "message": "no data"
        }, 422


class MeMailUpdateAPI(Resource):
    @allow(["user"])
    @use_args(me_mail_update_post)
    def post(self, data):
        if data.get('email'):
            send_verify_email_code(data.get('email'))

            return {}

        if data.get('verify_code'):
            new_email = verify_mail_change_code(data.get('verify_code'))
            if not new_email:
                return {
                    "message": "invalid code"
                }, 403

            g.current_user.email = new_email
            session.commit()

            return {}

        return {
            "message": "no data"
        }, 422


class MePassUpdateAPI(Resource):
    @allow(["user"])
    @use_args(me_pass_update_post)
    def post(self, data):
        if not g.current_user.verify_password(data.get('old_pass')):
            return {
                "message": "invalid password"
            }, 403

        g.current_user.hash_password(data.get('new_pass'))
        session.commit()
        return {}
