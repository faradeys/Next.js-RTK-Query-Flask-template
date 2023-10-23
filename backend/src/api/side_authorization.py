"""Sided auth, social networks auth."""
import requests
from flask import g, request, current_app
from flask_restful import Resource
from webargs.flaskparser import use_args

from src.db import db, session, redis
from src.db.models import User, Role, File
from src.schemas.authorization import vk_side_auth_post, fb_side_auth_post
from src.lib.access import redis_set


class VKSideAuthAPI(Resource):
    @use_args(vk_side_auth_post)
    def post(self,data):
        """recieve user data to get access through VK"""

        req = 'https://api.vk.com/method/apps.get?v=5.73&access_token={vk_token}'
        req = req.format(**dict(
            vk_token = data.get('access_token')
        ))
        resp = requests.get(req)

        if 'error' in resp.json() or not resp.json().get('response').get('items')[0].get('id') == current_app.config['VK_IMPLICIT_AUTH_APPID']:
            print('===api return fail or other app in use===')
            print(resp.json())
            return {
                "message": "not authorized"
            }, 401

        req = 'https://api.vk.com/method/users.get?v=5.73&fields=photo_200_orig&access_token={vk_token}'
        req = req.format(**dict(
            vk_token = data.get('access_token')
        ))
        resp = requests.get(req)

        if 'error' in resp.json():
            print('===api return fail===')
            print(resp.json())
            return {
                "message": "not authorized"
            }, 401

        side_data = resp.json().get('response')[0]
        user_data = {
            'side_id': 'VK:' + str(side_data.get('id')),
            'name': side_data.get('first_name')+' '+side_data.get('last_name'),
            'photo_url': side_data.get('photo_200_orig')
        }

        return auth_or_reg_sideuser(token=data.get('access_token'), user_data=user_data)


class FBSideAuthAPI(Resource):
    @use_args(fb_side_auth_post)
    def post(self,data):
        """recieve user data to get access through FB"""

        req = 'https://graph.facebook.com/v2.12/app?access_token={fb_token}'
        req = req.format(**dict(
            fb_token=data.get('access_token')
        ))
        resp = requests.get(req)

        if 'error' in resp.json() or not resp.json().get('id') == str(current_app.config['FB_IMPLICIT_AUTH_APPID']):
            print('===api return fail or other app in use===')
            print(resp.json())
            return {
                "message": "not authorized"
            }, 401

        req = 'https://graph.facebook.com/v2.12/me?fields=first_name,last_name,picture.height(200).width(200)&locale=ru_RU&access_token={fb_token}'
        req = req.format(**dict(
            fb_token = data.get('access_token')
        ))
        resp = requests.get(req)

        if 'error' in resp.json():
            print('===api return fail===')
            print(resp.json())
            return {
                "message": "not authorized"
            }, 401

        side_data = resp.json()
        user_data = {
            'side_id': 'FB:'+str(side_data.get('id')),
            'name': side_data.get('first_name')+' '+side_data.get('last_name'),
            'photo_url': side_data.get('picture').get('data').get('url')
        }

        return auth_or_reg_sideuser(token=data.get('access_token'), user_data=user_data)


def auth_or_reg_sideuser(token, user_data):
    """reg or auth user recieved from social network"""

    user = User.query.filter( db.or_(User.roles.any(name='user')) ).filter_by(side_id = user_data['side_id'], is_deleted=False).first()
    if not user:
        user = User(
            side_id=user_data['side_id'],
            name=user_data['name'],
            is_verified=True
        )
        user.add_role(Role.get_by_name('user'))
        session.add(user)
        session.commit()

        if user_data['photo_url']:
            side_img = requests.get(user_data['photo_url'])
            if side_img.ok and side_img.headers.get('Content-Type')[:6] == 'image/':
                stored_side_img = File.store(
                    created_by=user.id,
                    fullname=str(user.side_id).replace(':','')+'_avatar',
                    binary=side_img.content,
                    as_avatar=True
                )
                user.avatar = stored_side_img
                session.commit()

    used_side_token = redis.get(':'.join(['side_token', user.id]))
    if used_side_token and token == used_side_token.decode():
        print('===this token already used before, need to get new one===')
        return {
            "message": "not authorized"
        }, 401

    if user.is_banned:
        return {
            "message": "user with this account was banned"
        }, 423

    redis_key = ':'.join(['side_token', user.id])
    redis_set(redis_key, token, current_app.config['TOKEN_EXPIRATION'])  # make side token useable just once like access token

    return {
        'access_token': user.generate_auth_token()
    }