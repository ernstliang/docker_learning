# 密码散列化测试
import unittest
from app.models import User

DEF_PASSWORD = '123456'
DEF_PASSWORD2 = '123457'

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password = DEF_PASSWORD)
        self.assertTrue(u.password_hash is not None)
    
    def test_no_password_getter(self):
        u = User(password = DEF_PASSWORD)
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password = DEF_PASSWORD)
        self.assertTrue(u.verify_password(DEF_PASSWORD))
        self.assertFalse(u.verify_password(DEF_PASSWORD2))

    def test_password_salts_are_random(self):
        u = User(password = DEF_PASSWORD)
        u2 = User(password = DEF_PASSWORD)
        self.assertTrue(u.password_hash != u2.password_hash)
