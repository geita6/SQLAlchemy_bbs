from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.message import Messages

main = Blueprint('mail', __name__)


@main.route('/')
def index():
    u = current_user()

    send = Messages.all(sender_id=u.id)
    received = Messages.all(receiver_id=u.id)

    t = render_template(
        'mail/index.html',
        user=u,
        send=send,
        received=received,
    )
    return t


@main.route("/add", methods=["POST"])
def add():
    form = request.form.to_dict()
    u = current_user()
    print('send mail form ', form)
    receiver = User.one(username=form['receiver_name'])
    receiver_id = receiver.id
    # 发邮件
    Messages.send(
        title=form['title'],
        content=form['content'],
        sender_id=u.id,
        receiver_id=receiver_id
    )

    return redirect(url_for('mail.index'))


@main.route('/<int:id>')
def view(id):
    message = Messages.one(id=id)
    u = current_user()
    # if u.id == mail.receiver_id or u.id == mail.sender_id:
    if u.id in [message.receiver_id, message.sender_id]:
        receiver = User.one(id=message.receiver_id)
        sender = User.one(id=message.sender_id)
        return render_template('mail/detail.html', message=message, user=u, receiver=receiver, sender=sender)
    else:
        return redirect(url_for('mail.index'))
