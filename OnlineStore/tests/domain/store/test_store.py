from unittest import TestCase

from OnlineStore.src.domain.store.store import Store


class TestStore(TestCase):
    def setUp(self):
        self.store = Store('store', 'batman', {'own': 'batman'}, {'mngr': 'batman'})
        self.store.add_product_store({'product_id': 1, 'product_name': 'name', 'quantity': 1})

    def test_check_permission_to_edit_store_inventory(self):
        self.assertRaises(Exception, self.store.check_permission_to_edit_store_inventory, 'spiderman')
        self.assertTrue(self.store.check_permission_to_edit_store_inventory('batman'))
        self.assertTrue(self.store.check_permission_to_edit_store_inventory('own'))
        self.assertTrue(self.store.check_permission_to_edit_store_inventory('mngr'))

    def test_remove_product_from_store_inventory(self):
        self.assertRaises(Exception, self.store.remove_product_store, 2)
        self.store.remove_product_store(1)
        self.assertTrue(1 not in self.store.inventory.products_dict)

    def test_add_new_product_to_store_inventory(self):
        self.assertRaises(Exception, self.store.add_product_store,
                          {'product_id': 1, 'product_name': 'name', 'quantity': 1})
        self.store.add_product_store({'product_id': 2, 'product_name': 'name', 'quantity': 1})
        self.assertTrue(2 in self.store.inventory.products_dict and self.store.inventory.products_dict[2].quantity == 1)

    def test_edit_product(self):
        self.assertRaises(Exception, self.store.edit_product, 2, 'details')
        self.store.edit_product(1, 'details')
        self.assertTrue(self.store.inventory.products_dict[1].description == 'details')

    def test_check_permission_to_assign(self):
        self.assertFalse(self.store.check_permission_to_assign('spiderman'))
        self.assertTrue(self.store.check_permission_to_assign('batman'))
        self.assertTrue(self.store.check_permission_to_assign('own'))
        self.assertFalse(self.store.check_permission_to_assign('mngr'))

    def test_assign_new_owner(self):
        self.assertRaises(Exception, self.store.assign_new_owner, 'own', 'batman')
        self.store.assign_new_owner('own1', 'own')
        self.assertTrue('own1' in self.store.owners and self.store.owners['own1'] == 'own')
        self.store.assign_new_owner('mngr', 'own')
        self.assertTrue('mngr' in self.store.owners)
        self.assertTrue('mngr' not in self.store.managers)

    def test_assign_new_manager(self):
        self.assertRaises(Exception, self.store.assign_new_manager, 'mngr', 'batman')
        self.assertRaises(Exception, self.store.assign_new_manager, 'own', 'batman')
        self.store.assign_new_manager('mngr1', 'own')
        self.assertTrue('mngr1' in self.store.managers and self.store.managers['mngr1'] == 'own')

    def test_delete_manager(self):
        self.assertRaises(Exception, self.store.delete_manager, 'mngr', 'own')
        self.store.delete_manager('mngr', 'batman')
        self.assertTrue('mngr' not in self.store.managers)
