import re
from pytz import timezone
from uuid import UUID
import requests
from datetime import datetime


def get_config(name):
    return getattr(__import__('instance.config',
                              fromlist=[name]),
                   name)


def parse_phone(phone):
    if not phone:
        return None
    parsed_phone = re.sub('\(|\)|-|\s', '', phone)
    if parsed_phone[0] == '+':
        parsed_phone = parsed_phone[1:]
    if parsed_phone[0] == '8':
        parsed_phone = '7' + parsed_phone[1:]
    elif parsed_phone[0] == '7':
        return parsed_phone
    elif not parsed_phone[0] == '7':
        parsed_phone = '7' + parsed_phone
    return parsed_phone


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def safety_int(s):
    try:
        int(s)
        return int(s)
    except ValueError:
        return 0


def generate_short_url(url):

    short_domain = get_config('SHORT_URL')

    if not short_domain:
        return False

    req = short_domain + 'generate/{url_get}'
    req = req.format(**dict(
        url_get = url
    ))
    try:
        resp = requests.get(req)
    except requests.exceptions.ConnectionError:
        return False
    

    if not resp:
        return False

    if 'code' not in resp.json():
        return False

    return short_domain + resp.json().get('code')
