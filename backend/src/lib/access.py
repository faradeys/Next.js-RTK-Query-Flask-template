import random, string, json
from functools import wraps
from flask import current_app, g, render_template
from src.db import redis
from flask_login import LoginManager, current_user
from uuid import uuid4, UUID
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired,
)

login_manager = LoginManager()

def redis_set(key, value, exp=None):
    redis.set(key, value)
    if exp:
        redis.expire(key, int(exp))

def validate_uuid(uuid_string):
    if not uuid_string:
        return False
    try:
        val = UUID(uuid_string)
    except ValueError:
        return False
    return True

def allow(role_names):
    """Verification of access to the resource"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            access = False
            for role_name in role_names:
                access = access or g.current_user.verify_access(role_name)
            if access:
                return func(*args, **kwargs)
            return {
                "message": "user does not have access",
                "User": str(g.current_user.name)
            }, 403
        return wrapper
    return decorator

def allow_view(role_names):
    """Verification of access to the view"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            access = False
            for role_name in role_names:
                access = access or current_user.verify_access(role_name)
            if access:
                return func(*args, **kwargs)
            return render_template('admin_panel/login.html', err_msg='нет прав доступа')
        return wrapper
    return decorator


def auth_greenlight(func):
    def wrapper(*args, **kwargs):
        auth_tries = redis.get(':'.join(['auth_tries', g.user_ip]))
        if auth_tries:
            auth_tries = int(auth_tries.decode())
            if auth_tries < 1:
                return {
                    "message": "too many auth requests"
                }, 423
            redis_set(':'.join(['auth_tries', g.user_ip]), auth_tries - 1, current_app.config['BAD_AUTH_COOLDOWN'])
        if not auth_tries:
            redis_set(':'.join(['auth_tries', g.user_ip]), current_app.config['AUTH_TRIES'] - 1, current_app.config['BAD_AUTH_COOLDOWN'])
        return func(*args, **kwargs)
    return wrapper


def reset_pass_greenlight(func):
    def wrapper(*args, **kwargs):
        reset_pass_tries = redis.get(':'.join(['reset_pass_tries', g.user_ip]))
        if reset_pass_tries:
            reset_pass_tries = int(reset_pass_tries.decode())
            if reset_pass_tries < 1:
                return {
                    "message": "too many reset pass requests"
                }, 423
            redis_set(':'.join(['reset_pass_tries', g.user_ip]), reset_pass_tries - 1, current_app.config['RESET_PASS_COOLDOWN'])
        if not reset_pass_tries:
            redis_set(':'.join(['reset_pass_tries', g.user_ip]), current_app.config['RESET_PASS_TRIES'] - 1, current_app.config['RESET_PASS_COOLDOWN'])
        return func(*args, **kwargs)
    return wrapper


def invite_friend_greenlight(func):
    def wrapper(*args, **kwargs):
        invite_friend_tries = redis.get(':'.join(['invite_friend_tries', g.user_ip]))
        if invite_friend_tries:
            invite_friend_tries = int(invite_friend_tries.decode())
            if invite_friend_tries < 1:
                return {
                    "message": "too many invite friend requests"
                }, 423
            redis_set(':'.join(['invite_friend_tries', g.user_ip]), invite_friend_tries - 1, current_app.config['INVITE_FRIEND_COOLDOWN'])
        if not invite_friend_tries:
            redis_set(':'.join(['invite_friend_tries', g.user_ip]), current_app.config['INVITE_FRIEND_TRIES'] - 1, current_app.config['INVITE_FRIEND_COOLDOWN'])
        return func(*args, **kwargs)
    return wrapper


def validate_uuid(uuid_string):
    if not uuid_string:
        return False
    try:
        val = UUID(uuid_string)
    except ValueError:
        return False
    return True


def generate_token(uid):
    """generate JWT token"""

    genuine_token_id = str(uuid4())
    token_serializer = Serializer(current_app.config['SECRET_KEY'], expires_in=current_app.config['TOKEN_EXPIRATION'])
    token = token_serializer.dumps({
        'uid': uid,
        'token_id': genuine_token_id,
    }).decode('ascii')

    redis_key = ':'.join(['access_token', uid])
    redis_set(redis_key, genuine_token_id, current_app.config['TOKEN_EXPIRATION'])  # setting latest token couple version instead of the old
    redis.delete( ':'.join(['auth_tries', g.user_ip]) )

    return token


def verify_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        token_claimset = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid
    genuine_token_id = redis.get( ':'.join([ 'access_token',token_claimset['uid'] ]) )
    if not genuine_token_id or not token_claimset['token_id'] == genuine_token_id.decode():  # compare recieved token with genuine couple
        return None  # revoked token

    return token_claimset


def revoke_token(uid):
    """revoke token for specified user"""

    redis.delete( ':'.join([ 'access_token', uid ]) )


def generate_phone_change_code(phone):
    cooldown = redis.get(':'.join(['phone_change_cooldown', g.current_user.id]))
    if cooldown:
        return None

    change_phone_data = {
        'verify_code': ''.join([random.choice(string.digits) for n in range(4)]),
        'phone': phone
    }
    redis_set(':'.join(['phone_change_code', g.current_user.id]), json.dumps(change_phone_data), current_app.config['CHANGE_PHONE_CODE_EXPIRATION'])
    redis_set(':'.join(['phone_change_cooldown', g.current_user.id]), '1', current_app.config['CHANGE_PHONE_CODE_COOLDOWN'])
    return change_phone_data['verify_code']


def verify_phone_change_code(code):
    genuine_code = redis.get(':'.join(['phone_change_code', g.current_user.id]))
    if not genuine_code:
        return None
    genuine_code = json.loads(genuine_code.decode())
    if not str(code) == str(genuine_code['verify_code']):
        return None
    redis.delete(':'.join(['phone_change_code', g.current_user.id]))
    return genuine_code['phone']


def generate_mail_change_code(email):
    change_mail_data = {
        'verify_code': ''.join([random.choice(string.ascii_letters +string.digits) for n in range(6)]),
        'email': email
    }
    redis_set(':'.join(['mail_change_code', g.current_user.id]), json.dumps(change_mail_data), current_app.config['CHANGE_MAIL_CODE_EXPIRATION'])
    return change_mail_data['verify_code']


def verify_mail_change_code(code):
    genuine_code = redis.get(':'.join(['mail_change_code', g.current_user.id]))
    if not genuine_code:
        return None
    genuine_code = json.loads(genuine_code.decode())
    if not str(code) == str(genuine_code['verify_code']):
        return None
    redis.delete(':'.join(['mail_change_code', g.current_user.id]))
    return genuine_code['email']




# def generate_pass_reset_token(uid):
#     token_id = str(uuid4())
#     token_serializer = Serializer(current_app.config['SECRET_KEY'], expires_in=current_app.config['PASS_RESET_TOKEN_EXPIRATION'])
#     token = token_serializer.dumps({
#         'uid': uid,
#         'token_id': token_id
#     }).decode('ascii')
#
#     redis_key = ':'.join(['reset_pass_token', uid])
#     redis_set(redis_key, token_id, current_app.config['PASS_RESET_TOKEN_EXPIRATION'])
#
#     return token
#
#
# def verify_pass_reset_token(token):
#     s = Serializer(current_app.config['SECRET_KEY'])
#     try:
#         token_claimset = s.loads(token)
#     except SignatureExpired:
#         return None  # valid token, but expired
#     except BadSignature:
#         return None  # invalid
#     genuine_token_id = redis.get( ':'.join([ 'reset_pass_token', token_claimset['uid'] ]) )
#     if not genuine_token_id or not token_claimset['token_id'] == genuine_token_id.decode():  # compare recieved token with genuine id
#         return None  # used or invalid token
#
#     return token_claimset
