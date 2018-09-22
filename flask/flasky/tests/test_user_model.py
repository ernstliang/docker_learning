import unittest
from app.models import User, Role, Permission, AnonymousUser

class UserModelTestCase(unittest.TestCase):
    def test_role_and_permissions(self):
        Role.insert_roles()
        u = User(email='1917812891@qq.com', password='788569')
        self.assertTrue(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))