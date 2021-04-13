from unittest import TestCase

from OnlineStore.src.service.authentication import Authentication


class TestService(TestCase):
    def setUp(self):
        self.auth = Authentication()
        self.auth.register('admin', '123')

    def tearDown(self):
        self.auth = Authentication()

    def test_register(self):
        self.assertFalse(self.auth.register('admin', '123'))
        self.assertFalse(self.auth.register('admin', 'sdfgsdf'))
        self.assertTrue(self.auth.register('user', '123'))

    def test_login(self):
        self.assertTrue(self.auth.login('admin', '123'))
        self.assertFalse(self.auth.login('admin', 'sdfgsdf'))
        self.assertFalse(self.auth.login('user', '123'))
