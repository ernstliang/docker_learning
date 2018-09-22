#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Permission, Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.fake import users, posts

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Permission=Permission, Post=Post)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    '''
    Run the unit tests.
    '''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def create_db():
    '''
    create db and add roles
    '''
    db.drop_all()
    db.create_all()
    # 插入角色信息
    Role.insert_roles()
    # 添加admin用户信息
    User.insert_admin()
    User.insert_user()
    # 添加文章
    posts()

if __name__ == '__main__':
    manager.run()