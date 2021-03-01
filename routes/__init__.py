import uuid
from functools import wraps

from flask import (
    session,
    request,
    abort,
    redirect,
    url_for,
)

from models.user import User

from utils import log
# 导入redis，建立缓存
import redis

cache = redis.StrictRedis()


def current_user():
    if 'session_id' in request.cookies:
        session_id = request.cookies.get('session_id')
        key = 'session_id_{}'.format(session_id)
        user_id = cache.get(key)
        # log('current_user user_id <{}>'.format(user_id))
        if user_id is None:
            return User.guest()
        else:
            # print('in has session')
            uid = int(user_id.decode())
            u = User.one(id=uid)
            if u is None:
                return User.guest()
            else:
                return u
    else:
        return None


def login_required(route_function):
    @wraps(route_function)
    def f():
        log('login_required')
        u = current_user()
        if u is None:
            log('游客用户')
            return redirect(url_for('index.index'))
        else:
            log('登录用户', route_function)
            return route_function()

    return f


# csrf_tokens = dict()


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        # if token in csrf_tokens and csrf_tokens[token] == u.id:
        if cache.exists(token.encode()) and int(cache.get(token).decode()) == u.id:
            cache.delete(token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    # print('new_csrf_token, user', u)
    token = str(uuid.uuid4())
    cache.set(token, u.id)
    return token
