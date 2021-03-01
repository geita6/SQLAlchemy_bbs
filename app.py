#!/usr/bin/env python3
import time

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import secret
import config
from models.base_model import db
# from models.reply import Reply as rrrr
# from models.topic import Topic as tttt

from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.board import main as board_routes
from routes.message import main as mail_routes
from routes.setting import main as setting_routes
from routes.profile import main as profile_routes

from utils import log


def format_time(unix_timestamp):
    f = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(unix_timestamp)
    formatted = time.strftime(f, value)
    return formatted


def count(input):
    return len(input)


def time_dict(unix_timestamp):
    t = format_time(unix_timestamp)
    date_of_time = t.split(' ')[0].split('-')
    clock_of_time = t.split(' ')[1].split(':')
    time_dict = dict(
        year=int(date_of_time[0]),
        month=int(date_of_time[1]),
        day=int(date_of_time[2]),
        hour=int(clock_of_time[0]),
        minute=int(clock_of_time[1]),
        second=int(clock_of_time[2]),
    )
    return time_dict


def time_between_now(unix_timestamp):
    now = int(time.time())
    now_dict = time_dict(now)
    t_dict = time_dict(unix_timestamp)
    # log('t_dict and now_dict', t_dict, now_dict)
    year_from_now = now_dict['year'] - t_dict['year']
    month_from_now = now_dict['month'] - t_dict['month']
    day_from_now = now_dict['day'] - t_dict['day']
    hour_from_now = now_dict['hour'] - t_dict['hour']
    minute_from_now = now_dict['minute'] - t_dict['minute']
    second_from_now = now_dict['second'] - t_dict['second']

    if year_from_now > 0:
        return str(year_from_now) + "年前"
    elif month_from_now > 0:
        return str(month_from_now) + "个月前"
    elif day_from_now > 0:
        return str(day_from_now) + "天前"
    elif hour_from_now > 0:
        return str(hour_from_now) + "小时前"
    elif minute_from_now > 1:
        return str(minute_from_now) + "分钟前"
    elif second_from_now > 0:
        return str(second_from_now) + "秒前"


def configured_app():
    app = Flask(__name__)

    uri = 'mysql+pymysql://root:{}@localhost/bbs?charset=utf8mb4'.format(
        secret.database_password
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.template_filter()(format_time)
    app.template_filter()(count)
    app.template_filter()(time_between_now)

    register_routes(app)

    return app


def register_routes(app):
    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(mail_routes, url_prefix='/mail')
    app.register_blueprint(setting_routes, url_prefix='/setting')
    app.register_blueprint(profile_routes, url_prefix='/profile')


# 运行代码
if __name__ == '__main__':
    app = configured_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=2000,
        threaded=True,
    )
    app.run(**config)
