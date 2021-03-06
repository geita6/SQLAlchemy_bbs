from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    Request)

from models.message import Messages
from routes import *

from models.reply import Reply


main = Blueprint('reply', __name__)


def users_from_content(content):
    parts = content.split()
    users = []

    for p in parts:
        if p.startswith('@'):
            username = p[1:]
            u = User.one(username=username)
            # print('users_from_content <{}> <{}> <{}>'.format(username, p, parts))
            if u is not None:
                users.append(u)

    return users


def send_mails(sender, receivers, reply_link, reply_content):
    # print('send_mail', sender, receivers, reply_content)
    content = '链接：{}\n内容：{}'.format(
        reply_link,
        reply_content
    )
    for r in receivers:
        title = '你被 {} AT 了'.format(sender.username)
        Messages.send(
            title=title,
            content=content,
            sender_id=sender.id,
            receiver_id=r.id
        )


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()

    content = form['content']
    users = users_from_content(content)
    send_mails(u, users, request.referrer, content)

    form = form.to_dict()
    m = Reply.new(form, user_id=u.id)

    # 删除redis缓存
    k1 = 'created_topic_{}'.format(u.id)
    k2 = 'replied_topic_{}'.format(u.id)
    cache.delete(k1)
    cache.delete(k2)

    return redirect(url_for('topic.detail', id=m.topic_id))

