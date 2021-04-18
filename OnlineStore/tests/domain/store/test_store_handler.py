from unittest import TestCase

from OnlineStore.src.domain.store.product import Product
from OnlineStore.src.domain.store.store import Store
from OnlineStore.src.domain.store.store_handler import StoreHandler


class TestStoreHandler(TestCase):
    def setUp(self):
        self.handler = StoreHandler()
        self.handler.open_store('store', 'batman')
        self.handler.add_new_product_to_store_inventory('batman',
                                                        {'product_id': 1, 'product_name': 'prod name', 'quantity': 1,
                                                         'price': 10},
                                                        'store')

    def test_open_store(self):
        self.assertRaises(Exception, self.handler.open_store, 'store', 'admin')
        self.handler.open_store('store1', 'admin')
        self.assertTrue('store1' in self.handler.store_dict)

    def test_add_new_product_to_store_inventory(self):
        self.assertRaises(Exception, self.handler.add_new_product_to_store_inventory, 'batman',
                          {'product_id': 1, 'product_name': 'name', 'quantity': 1, 'price': 10}, 'no store')
        self.assertRaises(Exception, self.handler.add_new_product_to_store_inventory, 'batman',
                          {'product_id': 1, 'product_name': 'name', 'quantity': 1, 'price': 10}, 'store')
        self.assertRaises(Exception, self.handler.add_new_product_to_store_inventory, 'no permission',
                          {'product_id': 1, 'product_name': 'name', 'quantity': 1, 'price': 10}, 'store')
        self.handler.add_new_product_to_store_inventory('batman',
                                                        {'product_id': 2, 'product_name': 'name', 'quantity': 1,
                                                         'price': 10},
                                                        'store')
        self.assertTrue(2 in self.handler.store_dict['store'].inventory.products_dict)

    def test_remove_product_from_store_inventory(self):
        self.assertRaises(Exception, self.handler.remove_product_from_store_inventory, 'batman', 1, 'no store')
        self.assertRaises(Exception, self.handler.remove_product_from_store_inventory, 'no permission', 1, 'store')
        self.assertRaises(Exception, self.handler.remove_product_from_store_inventory, 'batman', 2, 'store')
        self.handler.remove_product_from_store_inventory('batman', 1, 'store')
        self.assertTrue(1 not in self.handler.store_dict['store'].inventory.products_dict)

    def test_get_information_about_products(self):
        self.assertRaises(Exception, self.handler.get_information_about_products, 'no store')
        for pid, prod in self.handler.get_information_about_products('store').items():
            print(f'id: {pid}, name: {prod.product_name}, quantity: {prod.quantity}, description: {prod.description}')

    def test_get_store_info(self):
        self.assertRaises(Exception, self.handler.get_store_info, 'no store')
        print(self.handler.get_store_info('store'))

    def test_get_store(self):
        self.assertRaises(Exception, self.handler.get_store, 'no store')
        self.assertTrue(type(self.handler.get_store('store')) == Store)

    def test_check_product_exists_in_store(self):
        self.assertRaises(Exception, self.handler.check_product_exists_in_store, 1, 'no store')
        self.assertRaises(Exception, self.handler.check_product_exists_in_store, 2, 'store')
        self.handler.remove_product_from_store_inventory('batman', 1, 'store')
        self.assertRaises(Exception, self.handler.check_product_exists_in_store, 1, 'store')

    def test_find_product_by_id(self):
        self.assertRaises(Exception, self.handler.find_product_by_id, 1, 'no store')
        self.assertRaises(Exception, self.handler.find_product_by_id, 2, 'store')
        self.assertTrue(type(self.handler.find_product_by_id(1, 'store')) == Product)

    # def test_is_manager_assigner(self):
    #     self.assertRaises(Exception, self.handler.find_product_by_id, 1, 'no store')

    # def test_get_store_purchase_history(self):
    #     self.assertRaises(Exception, self.handler.find_product_by_id, 1, 'no store')
