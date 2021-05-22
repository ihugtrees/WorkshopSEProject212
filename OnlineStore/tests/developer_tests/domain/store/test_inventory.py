from unittest import TestCase

from OnlineStore.src.domain_layer.store.inventory import Inventory


class TestInventory(TestCase):
    def setUp(self):
        self.inv = Inventory(dict())
        self.inv.add_product_inventory({'product_id': 1, 'product_name': 'name', 'quantity': 1, 'price': 10})

    def test_remove_product_inventory(self):
        self.assertRaises(Exception, self.inv.remove_product_inventory, 2)
        self.inv.remove_product_inventory(1)
        self.assertTrue(1 not in self.inv.products_dict)

    def test_add_product_inventory(self):
        self.assertRaises(Exception, self.inv.add_product_inventory,
                          {'product_id': 1, 'product_name': 'name', 'quantity': 1, 'price': 10})
        self.inv.add_product_inventory({'product_id': 2, 'product_name': 'name', 'quantity': 1, 'price': 10})
        self.assertTrue(2 in self.inv.products_dict and self.inv.products_dict[2].quantity == 1)
