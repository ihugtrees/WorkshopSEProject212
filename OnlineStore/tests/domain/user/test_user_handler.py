from unittest import TestCase

from OnlineStore.src.domain.user.user_handler import UserHandler


class TestUserHandler(TestCase):
    def setUp(self):
        self.user_handler = UserHandler()
        self.user_handler.register('admin')

    def test_register(self):
        self.assertRaises(Exception, self.user_handler.register, 'admin')
        self.user_handler.register('batman')
        self.assertTrue('batman' in self.user_handler.users_dict)

    def test_login(self):
        self.assertRaises(Exception, self.user_handler.login, 'batman')
        self.user_handler.login('admin')
        self.assertTrue(self.user_handler.users_dict['admin'].is_logged)

    def test_logout(self):
        self.assertRaises(Exception, self.user_handler.logout, 'batman')
        self.assertRaises(Exception, self.user_handler.logout, 'admin')
        self.user_handler.login('admin')
        self.assertTrue(self.user_handler.users_dict['admin'].is_logged)
        self.user_handler.logout('admin')
        self.assertFalse(self.user_handler.users_dict['admin'].is_logged)

    def test_add_product(self):
        self.assertRaises(Exception, self.user_handler.add_product, 'batman', 1, 1, 1)
        self.user_handler.add_product('admin', 1, 1, 1)
        self.assertTrue(1 in self.user_handler.users_dict['admin'].cart.basket_dict)
        self.assertTrue(1 in self.user_handler.users_dict['admin'].cart.basket_dict[1].products_dict)
        self.assertTrue(1 == self.user_handler.users_dict['admin'].cart.basket_dict[1].products_dict[1])

    def test_remove_product(self):
        self.assertRaises(Exception, self.user_handler.add_product, 'batman', 1, 1, 1)
        self.user_handler.add_product('admin', 1, 1, 1)
        self.assertTrue(1 in self.user_handler.users_dict['admin'].cart.basket_dict)
        self.assertTrue(1 in self.user_handler.users_dict['admin'].cart.basket_dict[1].products_dict)
        self.assertTrue(1 == self.user_handler.users_dict['admin'].cart.basket_dict[1].products_dict[1])
        self.user_handler.remove_product('admin', 1, 1, 1)
        self.assertTrue(1 in self.user_handler.users_dict['admin'].cart.basket_dict)
        self.assertFalse(1 in self.user_handler.users_dict['admin'].cart.basket_dict[1].products_dict)

    def test_get_cart(self):
        self.fail() # TODO IMBLEMENT
