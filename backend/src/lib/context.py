from utils import get_config
import requests
from flask import _request_ctx_stack, g
from src.db.models import ALL_MODELS
from src.db import session, db


def shel_context():
    """Контекст Ipython для быстрой удобной отладки"""
    context = {}
    context['app'] = _request_ctx_stack.top.app
    context['session'] = session
    context['get_config'] = get_config
    context['db'] = db
    context['g'] = g
    context['requests'] = requests
    context.update(ALL_MODELS)
    g.test = {}

    # try:
    #     User = ALL_MODELS.get('User')
    #     context['user'] = User.query.filter(User.phone == '9876543210').first()
    # except:
    #     pass

    return context
