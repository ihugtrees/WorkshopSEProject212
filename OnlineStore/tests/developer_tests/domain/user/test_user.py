from unittest import TestCase

from OnlineStore.src.domain_layer.user.cart import Cart
from OnlineStore.src.domain_layer.user.user import User


class TestUser(TestCase):
    def setUp(self):
        self.admin = User('admin', 30, Cart(), True)
        self.user = User('admin', 30, Cart())
        self.user.add_product_to_user(1, 1, 1)

    def test_login(self):
        self.assertFalse(self.user.is_logged)
        self.user.login()
        self.assertTrue(self.user.is_logged)

    def test_logout(self):
        self.assertFalse(self.user.is_logged)
        self.user.login()
        self.assertTrue(self.user.is_logged)
        self.user.logout()
        self.assertFalse(self.user.is_logged)

    def test_is_admin(self):
        self.assertFalse(self.user.is_admin())
        self.assertTrue(self.admin.is_admin())

    def test_add_product_to_user(self):
        self.assertRaises(Exception, self.user.add_product_to_user, 1, 1, 0)
        self.assertRaises(Exception, self.user.add_product_to_user, 1, 1, -1)
        self.user.add_product_to_user(1, 1, 1)
        self.assertTrue(self.user.cart.basket_dict[1].products_dict[1] == 2)
        self.user.add_product_to_user(1, 2, 1)
        self.assertTrue(self.user.cart.basket_dict[1].products_dict[2] == 1)
        self.user.add_product_to_user(2, 2, 2)
        self.assertTrue(self.user.cart.basket_dict[2].products_dict[2] == 2)

    def test_remove_product_from_user(self):
        self.assertRaises(Exception, self.user.remove_product_from_user, 2, 1, 1)
        self.assertRaises(Exception, self.user.remove_product_from_user, 1, 2, 1)
        self.assertRaises(Exception, self.user.remove_product_from_user, 1, 1, 0)
        self.assertRaises(Exception, self.user.remove_product_from_user, 2, 1, -1)
        self.user.add_product_to_user(1, 1, 1)
        self.assertTrue(self.user.cart.basket_dict[1].products_dict[1] == 2)
        self.user.remove_product_from_user(1, 1, 1)
        self.assertTrue(self.user.cart.basket_dict[1].products_dict[1] == 1)
        self.user.remove_product_from_user(1, 1, 1)
        self.assertRaises(Exception, self.user.remove_product_from_user, 1, 1, 1)
        self.user.add_product_to_user(2, 2, 2)
        self.user.remove_product_from_user(2, 2, 1)
        self.assertTrue(self.user.cart.basket_dict[2].products_dict[2] == 1)
