import re
import unittest
from app import create_app, db
from app.models import User, Role

EMAIL_USER = '1917812891@qq.com'
PASWD_1 = '123456'

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Stranger' in response.get_data(as_text=True))

    def test_register_and_login(self):
        response = self.client.post('/auth/register', data={
            'email': EMAIL_USER,
            'username': 'john',
            'password': PASWD_1,
            'password2': PASWD_1
        })
        self.assertEqual(response.status_code, 302)
        # print('register: ', response.get_data(as_text=True))

        response = self.client.post('/auth/login', data={
            'email': EMAIL_USER,
            'password': PASWD_1
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(re.search('Hello,\s+john!', response.get_data(as_text=True)))
        self.assertTrue('You have not confirmed your account yet.' in response.get_data(as_text=True))

        user = User.query.filter_by(email=EMAIL_USER).first()
        token = user.generate_confirmation_token()
        response = self.client.get('/auth/confirm/{}'.format(token), follow_redirects=True)
        user.confirm(token)
        self.assertEqual(response.status_code, 200)
        # print(response.get_data(as_text=True))
        self.assertTrue('You have not confirmed your account yet.' in response.get_data(as_text=True))

        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('You have been logged out' in response.get_data(as_text=True))