import hashlib

from sqlalchemy import Column, String, Text

import config
import secret
from models.base_model import SQLMixin, db
from models.user_role import UserRole


class User(SQLMixin, db.Model):
    __tablename__ = 'User'

    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    image = Column(String(100), nullable=False, default='/images/user0.jpg')
    email = Column(String(50), nullable=False, default=config.test_mail)
    signature = Column(String(256), nullable=False, default='这是签名')
    # role = Column(String(50), nullable=False, default=UserRole.normal)

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        print('register', form)
        if len(name) > 2 and User.one(username=name) is None:
            form['password'] = User.salted_password(form['password'])
            u = User.new(form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        # print('form', form)
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )
        # print('validate_login', form, query)
        return User.one(**query)

    @staticmethod
    def guest():
        u = User()
        u.username = '【游客】'
        return u

