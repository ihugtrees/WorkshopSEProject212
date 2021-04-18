from unittest import TestCase

from OnlineStore.src.security.authentication import Authentication


class TestService(TestCase):
    def setUp(self):
        self.auth = Authentication()
        self.auth.register('admin', '123')

    def test_register(self):
        self.assertRaises(Exception, self.auth.register, 'admin', '123')
        self.assertRaises(Exception, self.auth.register, 'admin', 'wrong pass')
        hashed_username = self.auth.register('user', '123')
        self.assertTrue(hashed_username in self.auth._hash_to_name)
        self.assertFalse(self.auth.users[hashed_username])

    def test_login(self):
        self.assertRaises(Exception, self.auth.login, 'user', '123')
        self.assertRaises(Exception, self.auth.login, 'admin', 'wrong pass')
        hashed_username = self.auth.login('admin', '123')
        self.assertTrue(self.auth.users[hashed_username])

    def test_authenticate_session(self):
        self.assertRaises(Exception, self.auth.authenticate_session, 'user', '123')
        self.assertRaises(Exception, self.auth.authenticate_session, 'admin', '123')
        hashed_username = self.auth.login('admin', '123')
        self.assertTrue(self.auth.users[hashed_username])

    def test_logout(self):
        hashed_username = self.auth.login('admin', '123')
        self.assertTrue(self.auth.users[hashed_username])
        self.auth.logout(hashed_username)
        self.assertFalse(self.auth.users[hashed_username])

    def test_guest_registering(self):
        self.auth.guest_registering('guest')
        self.assertTrue(self.auth.users['guest'])
        self.assertTrue(self.auth._hash_to_name['guest'] == 'guest')
