import json

from flask import (
    url_for,
    redirect,
    abort,
    render_template,
    Blueprint,
)

from models.reply import Reply
from models.topic import Topic
from models.user import User
from routes import current_user, cache, login_required

main = Blueprint('profile', __name__)


# 需要在添加删除修改帖子时删除redis缓存
def created_topic(user_id):
    k = 'created_topic_{}'.format(user_id)
    if cache.exists(k):
        # print('has redis')
        v = cache.get(k)
        ts = json.loads(v)
        # 实例化
        ts = [Topic(**t) for t in ts]
        return ts
    else:
        # print('no redis')
        ts = Topic.all(user_id=user_id)
        v = json.dumps([t.json() for t in ts])
        cache.set(k, v)

        return ts


def replied_topic(user_id):
    k = 'replied_topic_{}'.format(user_id)
    if cache.exists(k):
        v = cache.get(k)
        ts = json.loads(v)
        ts = [Topic(**t) for t in ts]
        return ts
    else:
        '''
        join语句解决n+1问题
        sql实现
        Topic.select()
          .join(Reply,'id','topic_id')
          .where(user_id=user_id)
          .all()
        '''
        ts = Topic.select_replied_topic(user_id)
        v = json.dumps([t.json() for t in ts])
        cache.set(k, v)
        return ts


@main.route('/')
@login_required
def index():
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    else:
        return redirect(url_for('profile.user_detail', id=u.id))


@main.route('/<int:id>')
def user_detail(id):
    u = User.one(id=id)
    if u is None:
        abort(404)
    else:
        created = created_topic(u.id)
        replied = replied_topic(u.id)
        return render_template(
            'profile.html',
            user=u,
            created=created,
            replied=replied,
        )
