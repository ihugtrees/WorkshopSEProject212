from unittest import TestCase

from OnlineStore.src.domain_layer.store.product import Product


class TestProduct(TestCase):
    def setUp(self):
        self.prod = Product(1, 'name', 1, 10)

    def test_take_quantity(self):
        self.assertRaises(Exception, self.prod.take_quantity, 0)
        self.prod.take_quantity(1)
        self.assertTrue(self.prod.quantity == 0)
        self.assertRaises(Exception, self.prod.take_quantity, 1)

    def test_add_quantity(self):
        self.assertRaises(Exception, self.prod.add_quantity, 0)
        self.prod.add_quantity(1)
        self.assertTrue(self.prod.quantity == 2)

    def test_edit_product_description(self):
        self.assertRaises(Exception, self.prod.edit_product_details, 1)
        self.assertTrue(self.prod.description == '')
        self.prod.edit_product_details('prod')
        self.assertTrue(self.prod.description == 'prod')
