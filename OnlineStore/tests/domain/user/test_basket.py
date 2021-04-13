from unittest import TestCase

from OnlineStore.src.domain.user.basket import Basket


class TestBasket(TestCase):
    def setUp(self):
        self.basket = Basket()
        self.basket.add_product_to_basket(1, 1)

    def test_add_product(self):
        self.assertRaises(Exception, self.basket.add_product_to_basket, 1, 0)
        self.assertRaises(Exception, self.basket.add_product_to_basket, 1, -1)
        self.basket.add_product_to_basket(1, 1)
        self.assertTrue(self.basket.products[1] == 2)
        self.basket.add_product_to_basket(2, 1)
        self.assertTrue(self.basket.products[2] == 1)

    def test_remove_product(self):
        self.assertRaises(Exception, self.basket.remove_product_from_basket, 1, 0)
        self.assertRaises(Exception, self.basket.remove_product_from_basket, 1, -1)
        self.assertRaises(Exception, self.basket.remove_product_from_basket, 1, 2)
        self.assertRaises(Exception, self.basket.remove_product_from_basket, 2, 1)
        self.basket.add_product_to_basket(1, 1)
        self.basket.remove_product_from_basket(1, 1)
        self.assertTrue(self.basket.products[1] == 1)
        self.basket.remove_product_from_basket(1, 1)
        self.assertRaises(Exception, self.basket.remove_product_from_basket, 1, 1)

    def test_get_product_dict(self):
        prods = {1: 1}
        self.assertEqual(self.basket.products, prods)
