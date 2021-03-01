from sqlalchemy import create_engine

import secret
from app import configured_app
from models.base_model import db
from models.board import Board
from models.reply import Reply
from models.topic import Topic
from models.user import User


def reset_database():
    # 现在 mysql root 默认用 socket 来验证而不是密码
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(
        secret.database_password
    )
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS bbs')
        c.execute('CREATE DATABASE bbs CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE bbs')

    db.metadata.create_all(bind=e)


def generate_fake_date():
    # 用户
    user1 = dict(
        username='abc',
        password='123',
        image='/images/user1.jpg',
        signature='就一会了'
    )
    u1 = User.register(user1)
    user2 = dict(
        username='xyz',
        password='890',
        image='/images/user2.jpg',
        signature='明天做'
    )
    u2 = User.register(user2)
    user3 = dict(
        username='cba',
        password='321',
        image='/images/user3.jpg',
        signature='做不完了'
    )
    u3 = User.register(user3)

    print('u1.id', u1.id)
    # 版块
    board1 = dict(
        title='外野'
    )
    b1 = Board.new(board1)
    board2 = dict(
        title='内野'
    )
    b2 = Board.new(board2)
    board3 = dict(
        title='护城河'
    )
    b3 = Board.new(board3)
    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()

    topic_form1 = dict(
        title='demo',
        board_id=b1.id,
        content=content
    )

    topic_form2 = dict(
        title='打 7',
        board_id=b2.id,
        content='7777777'
    )

    topic_form3 = dict(
        title='绿皮车',
        board_id=b3.id,
        content='内燃机车'
    )


    # for i in range(3):
    # print('begin topic <{}>'.format(i))
    t1 = Topic.new(topic_form1, u1.id)
    t2 = Topic.new(topic_form2, u2.id)
    t3 = Topic.new(topic_form3, u3.id)

    reply_form = dict(
        content='''
        | Tables        | Are           | Cool  |
        | ------------- |:-------------:| -----:|
        | col 3 is      | right-aligned |  |
        | col 2 is      | centered      |    |
        | zebra stripes | are neat      |     |
        ''',
        topic_id=t1.id,
    )
    Reply.new(reply_form, u1.id)
    reply_form = dict(
        content='不是',
        topic_id=t1.id,
    )
    Reply.new(reply_form, u2.id)
    reply_form = dict(
        content='没有，别瞎说',
        topic_id=t1.id,
    )
    Reply.new(reply_form, u3.id)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_date()
