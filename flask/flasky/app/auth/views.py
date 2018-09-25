from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .forms import LoginForm, ReqistationForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm
from .. import db
from ..email import send_email

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or passowrd.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = ReqistationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        # print('user is: ', user)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        # 邮件确认后更新数据库信息
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

# 前置判断用户是否确认
@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
            # print('endpoint is: %s' % request.endpoint)
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

# 重新发送确认邮件
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

# 修改密码
@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldpassword.data):
            print('old password_hash: %s' % current_user.password_hash)
            # 很奇怪直接改current_user.password会不成功，需要这样转一道
            user = User()
            user.password = form.newpassword.data
            current_user.password_hash = user.password_hash
            print('new password_hash: %s' % current_user.password_hash)
            db.session.add(current_user)
            db.session.commit()
        # 先取用户信息
        # user = User.query.filter_by(email=current_user.email).first()
        # # 校验旧密码是否正确
        # if user is not None and user.verify_password(form.oldpassword.data):
        # # if current_user.verify_password(form.oldpassword.data):
        #     # 替换新密码
        #     user.passowrd = form.newpassword.data
        #     print('new password_hash: %s' % user.password_hash)
        #     db.session.add(user)
        #     db.session.commit()
            flash('Your password is changed!')
            return redirect(url_for('main.index'))
        else:
            flash('password error or new password is not confirm')
    return render_template('auth/changepassword.html', form=form)

# 发送重置密码邮件
@auth.route('/reset', methods=['GET', 'POST'])
def reset_password_request():
    # 匿名用户
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        # 根据邮箱查找用户信息
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            token = user.generate_reset_token()
            send_email(form.email.data, 'Reset your password', 'auth/email/resetpassword', user=user, token=token)
            flash('A Reset password email has been send to you!')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email')
    return render_template('auth/resetpassword.html', form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        # 更新密码
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your passwod has been updated')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/resetpassword.html', form=form)
