import uuid

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
    current_app, send_from_directory)

import config
from models.message import send_mail
from models.user import User
from routes import current_user, cache

from utils import log

main = Blueprint('index', __name__)


# 登录
@main.route("/")
def index():
    u = current_user()
    return render_template("user/login_view.html")


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('index.index'))
    else:
        session_id = str(uuid.uuid4())
        key = 'session_id_{}'.format(session_id)
        log('index login <{}> <{}>'.format(key, u.id))
        cache.set(key, u.id)

        redirect_to_index = redirect(url_for('topic.index'))
        response = current_app.make_response(redirect_to_index)
        response.set_cookie('session_id', value=session_id)
        return response


# 注册
@main.route("/register_view")
def register_view():
    return render_template("user/register_view.html")


@main.route("/register", methods=['POST'])
def register():
    form = request.form.to_dict()
    # 用类函数来判断
    u = User.register(form)
    return redirect(url_for('index.index'))


# 重置密码
@main.route("/reset_commit_view")
def reset_commit_view():
    return render_template("user/reset_view.html")


@main.route("/reset_send", methods=['POST'])
def reset_send():
    form = request.form.to_dict()
    username = form['username']
    mail = form['to_mail']
    #  根据用户名拿到 user 对象
    u = User.one(username=username)
    token_id = str(uuid.uuid4())
    if u is not None:
        cache[token_id] = u.id
        # 给 user.email 的邮箱发邮件，发信人是企业邮箱，
        content = '重置密码地址 {}{}?token_id={}'.format(
            config.ip,
            url_for('index.reset_view'),
            token_id
        )
        send_mail(
            subject='重置密码',
            author=config.admin_mail,
            to=mail,
            content=content
        )
        return redirect(url_for('index.index'))
    else:
        abort(401)


@main.route("/reset/view")
def reset_view():
    log('request.args', request.args['token_id'])
    token_id = request.args['token_id']
    if cache.exists(token_id.encode()):
        # 点确定发请求到 /reset/update?token_id=token_id
        return render_template(
            'user/reset_pass.html',
            token_id=token_id,
        )
    else:
        log('token_id not exist', token_id)
        abort(401)


@main.route("/reset/update", methods=['POST'])
def reset_update():
    token_id = request.args['token_id']

    # 如果 token 存在通过对应 user_id 拿到 user 对象
    # if cache.exists(token.encode()) and int(cache.get(token).decode()) == u.id:
    # user_id = token.get(token_id, None)
    user_id = int(cache.get(token_id).decode())
    if user_id is None:
        log('token not found', token_id)
        abort(401)
    else:
        # 两次密码一致才可以更改
        if request.form['confirm_pass'] == request.form['new_pass']:
            password = request.form['confirm_pass']
            # 密码要加盐
            User.update(user_id, password=User.salted_password(password))
            return redirect(url_for('index.index'))
        else:
            # flash('请重新输入')
            return redirect(url_for('index.reset_view'))


@main.route('/images/<filename>')
def image(filename):
    return send_from_directory('images', filename)
