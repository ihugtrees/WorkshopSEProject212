from unittest import TestCase

from OnlineStore.src.domain.user.cart import Cart
from OnlineStore.src.domain.user.user import User


class TestUser(TestCase):
    def setUp(self):
        self.admin = User('admin', Cart(), True)
        self.user = User('admin', Cart())
        self.user.add_product_to_user(1, 1, 1)

    def test_login(self):
        self.assertFalse(self.user.logged_in)
        self.user.login()
        self.assertTrue(self.user.logged_in)

    def test_logout(self):
        self.assertFalse(self.user.logged_in)
        self.user.login()
        self.assertTrue(self.user.logged_in)
        self.user.logout()
        self.assertFalse(self.user.logged_in)

    def test_is_admin(self):
        self.assertFalse(self.user.is_admin())
        self.assertTrue(self.admin.is_admin())

    def test_add_product_to_user(self):
        self.assertRaises(Exception, self.user.add_product_to_user, 1, 1, 0)
        self.assertRaises(Exception, self.user.add_product_to_user, 1, 1, -1)
        self.user.add_product_to_user(1, 1, 1)
        self.assertTrue(self.user.cart.basket_dict[1].products[1] == 2)
        self.user.add_product_to_user(1, 2, 1)
        self.assertTrue(self.user.cart.basket_dict[1].products[2] == 1)
        self.user.add_product_to_user(2, 2, 2)
        self.assertTrue(self.user.cart.basket_dict[2].products[2] == 2)

    def test_remove_product_from_user(self):
        self.assertRaises(Exception, self.user.remove_product_from_user, 2, 1, 1)
        self.assertRaises(Exception, self.user.remove_product_from_user, 1, 2, 1)
        self.assertRaises(Exception, self.user.remove_product_from_user, 1, 1, 0)
        self.assertRaises(Exception, self.user.remove_product_from_user, 2, 1, -1)
        self.user.add_product_to_user(1, 1, 1)
        self.assertTrue(self.user.cart.basket_dict[1].products[1] == 2)
        self.user.remove_product_from_user(1, 1, 1)
        self.assertTrue(self.user.cart.basket_dict[1].products[1] == 1)
        self.user.remove_product_from_user(1, 1, 1)
        self.assertRaises(Exception, self.user.remove_product_from_user, 1, 1, 1)
        self.user.add_product_to_user(2, 2, 2)
        self.user.remove_product_from_user(2, 2, 1)
        self.assertTrue(self.user.cart.basket_dict[2].products[2] == 1)
