import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)
from werkzeug.datastructures import FileStorage

from models.user import User
from routes import current_user, login_required

main = Blueprint('setting', __name__)


# 设置页面
@main.route('/')
@login_required
def index():
    u = current_user()
    return render_template('setting.html', user=u)


# 修改用户名和签名
@main.route("/change_intro", methods=['POST'])
def change_intro():
    form = request.form.to_dict()
    u = current_user()
    User.update(u.id, username=form['name'])
    User.update(u.id, signature=form['signature'])
    return render_template('setting.html', user=u)


# 修改密码
@main.route("/change_pass", methods=['POST'])
def change_pass():
    form = request.form.to_dict()
    u = current_user()
    # 原密码正确才可以更改密码
    if u.password == User.salted_password(form['old_pass']):
        User.update(u.id, password=User.salted_password(form['new_pass']))
    return render_template('setting.html', user=u)


# 更换头像
@main.route('/image/add', methods=['POST'])
def avatar_add():
    file: FileStorage = request.files['avatar']
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)

    file.save(path)

    u = current_user()
    User.update(u.id, image='../images/{}'.format(filename))

    return redirect(url_for('setting.index'))
