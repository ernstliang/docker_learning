import os
from flask import Flask, render_template, session, redirect, url_for, flash
# bootstrap
from flask_bootstrap import Bootstrap
# wtf
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
# sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# migrate
from flask_script import Shell
from flask_migrate import Migrate, MigrateCommand
# mail
from flask_mail import Mail, Message
from threading import Thread

# 当前目录，可用于sqlite保存位置
basedir = os.path.abspath(os.path.dirname(__file__))

# flask app
app = Flask(__name__)
# wtf密钥
app.config['SECRET_KEY'] = '070D6501-E6B4-4295-AC43-8B58E2C999B9'
# sqlite存储配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# mail
app.config['MAIL_DEBUG'] = True
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = os.environ.get('MAIL_USERNAME')

# bootstrap网页组件框架
bootstrap = Bootstrap(app)
# sqlalchemy
db = SQLAlchemy(app)
# migrate
migrate = Migrate(app, db)
# mail
mail = Mail(app)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, User=User, Role=Role)

# 名字表单
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
    sendmail = SubmitField('SendMail')

# sqlalchemy数据结构
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

def sync_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=sync_send_mail, args=[app, msg])
    thr.start()
    return str

# 404错误页
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 500错误页
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('It Looks like you have changed your name to %s!' % form.name.data)
        session['name'] = form.name.data
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', 
            form=form, 
            name=session.get('name'),
            known=session.get('known', False))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    app.run()