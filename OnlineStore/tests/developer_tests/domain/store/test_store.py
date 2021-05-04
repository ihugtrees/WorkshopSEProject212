from unittest import TestCase

from OnlineStore.src.domain.store.store import Store


class TestStore(TestCase):
    def setUp(self):
        self.store = Store('store', 'batman', {'own': 'batman'}, {'mngr': 'batman'})
        self.store.add_product_store({'product_id': 1, 'product_name': 'name', 'quantity': 1, 'price': 10})

    def test_remove_product_from_store_inventory(self):
        self.assertRaises(Exception, self.store.remove_product_store, 2)
        self.store.remove_product_store(1)
        self.assertTrue(1 not in self.store.inventory.products_dict)

    def test_add_new_product_to_store_inventory(self):
        self.assertRaises(Exception, self.store.add_product_store,
                          {'product_id': 1, 'product_name': 'name', 'quantity': 1, 'price': 10})
        self.store.add_product_store({'product_id': 2, 'product_name': 'name', 'quantity': 1, 'price': 10})
        self.assertTrue(2 in self.store.inventory.products_dict and self.store.inventory.products_dict[2].quantity == 1)

    def test_edit_product(self):
        self.assertRaises(Exception, self.store.edit_product, 2, 'details')
        self.store.edit_product(1, 'details')
        self.assertTrue(self.store.inventory.products_dict[1].description == 'details')

