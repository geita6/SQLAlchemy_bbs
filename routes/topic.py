import time

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.reply import Reply
from routes import *

from models.topic import Topic
from models.board import Board

main = Blueprint('topic', __name__)


@main.route("/")
@login_required
def index():
    u = current_user()
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    token = new_csrf_token()
    bs = Board.all()
    return render_template("topic/index.html", ms=ms, token=token, bs=bs, bid=board_id, user=u)


@main.route('/<int:id>')
def detail(id):
    u = current_user()
    m = Topic.get(id)
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m, user=u)


@main.route("/delete")
@csrf_required
def delete():
    id = int(request.args.get('id'))
    u = current_user()
    # print('删除 topic 用户是', u, id)
    Topic.delete(id)

    re = Reply.all(topic_id=id)
    for r in re:
        Reply.delete(r.id)

    # 删除redis缓存
    k1 = 'created_topic_{}'.format(u.id)
    k2 = 'replied_topic_{}'.format(u.id)
    cache.delete(k1)
    cache.delete(k2)

    return redirect(url_for('.index'))


@main.route("/new")
def new():
    u = current_user()
    board_id = int(request.args.get('board_id', -1))
    bs = Board.all()
    # return render_template("topic/new.html", bs=bs, bid=board_id)
    token = new_csrf_token()
    return render_template("topic/new.html", bs=bs, token=token, bid=board_id, user=u)


@main.route("/add", methods=["POST"])
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    Topic.new(form, user_id=u.id)

    # 删除redis缓存
    k1 = 'created_topic_{}'.format(u.id)
    k2 = 'replied_topic_{}'.format(u.id)
    cache.delete(k1)
    cache.delete(k2)

    return redirect(url_for('topic.index'))


def new_reply_t(self):
    replies = Reply.all(topic_id=self.id)
    sorted_replies = sorted(replies, key=lambda r: r.created_time, reverse=True)
    # print('sorted_replies', sorted_replies)
    if len(sorted_replies) > 0:
        new_reply = sorted_replies[0]
        new_t = new_reply.created_time
        pass_t = (int(time.time()) - new_t)
        return pass_t
    else:
        return None
