from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app

from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        print('===== user is:')
        print(user)
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            # 新增加User时发送邮件通知Admin
            print('FLASKY_ADMIN is %s' % current_app.config['FLASKY_ADMIN'])
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['known'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html', 
            form=form, 
            name=session.get('name'),
            known=session.get('known', False))