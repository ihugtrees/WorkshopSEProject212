from unittest import TestCase

from OnlineStore.src.domain.user.cart import Cart


class TestCart(TestCase):
    def setUp(self):
        self.cart = Cart()
        self.cart.add_product_to_cart(1, 1, 1)

    def test_add_product_to_cart(self):
        self.assertRaises(Exception, self.cart.add_product_to_cart, 1, 1, 0)
        self.assertRaises(Exception, self.cart.add_product_to_cart, 1, 1, -1)
        self.cart.add_product_to_cart(1, 1, 1)
        self.assertTrue(self.cart.basket_dict[1].products[1] == 2)
        self.cart.add_product_to_cart(1, 2, 1)
        self.assertTrue(self.cart.basket_dict[1].products[2] == 1)
        self.cart.add_product_to_cart(2, 2, 2)
        self.assertTrue(self.cart.basket_dict[2].products[2] == 2)

    def test_remove_product_from_cart(self):
        self.assertRaises(Exception, self.cart.remove_product_from_cart, 2, 1, 1)
        self.assertRaises(Exception, self.cart.remove_product_from_cart, 1, 2, 1)
        self.assertRaises(Exception, self.cart.remove_product_from_cart, 1, 1, 0)
        self.assertRaises(Exception, self.cart.remove_product_from_cart, 2, 1, -1)
        self.cart.add_product_to_cart(1, 1, 1)
        self.cart.remove_product_from_cart(1, 1, 1)
        self.assertTrue(self.cart.basket_dict[1].products[1] == 1)
        self.cart.remove_product_from_cart(1, 1, 1)
        self.assertRaises(Exception, self.cart.remove_product_from_cart, 1, 1, 1)
        self.cart.add_product_to_cart(2, 2, 2)
        self.cart.remove_product_from_cart(2, 2, 1)
        self.assertTrue(self.cart.basket_dict[2].products[2] == 1)
