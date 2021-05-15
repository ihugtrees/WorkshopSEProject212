from unittest import TestCase

from OnlineStore.src.domain_layer.user.user_handler import UserHandler
import OnlineStore.src.data_layer.users_data as users

user_handler = UserHandler()


class TestUserHandler(TestCase):
    def setUp(self):
        global user_handler
        user_handler.register('admin')

    def tearDown(self) -> None:
        users.users = dict()

    def test_register(self):
        global user_handler
        self.assertRaises(Exception, user_handler.register, 'admin')
        user_handler.register('batman')
        self.assertTrue('batman' in users.users)

    def test_login(self):
        self.assertRaises(Exception, user_handler.login, 'batman')
        user_handler.login('admin')
        self.assertTrue(users.get_user_by_name("admin").is_logged)

    def test_logout(self):
        self.assertRaises(Exception, user_handler.logout, 'batman')
        self.assertRaises(Exception, user_handler.logout, 'admin')
        user_handler.login('admin')
        self.assertTrue(users.get_user_by_name('admin').is_logged)
        user_handler.logout('admin')
        self.assertFalse(users.get_user_by_name('admin').is_logged)

    def test_add_product(self):
        self.assertRaises(Exception, user_handler.add_product, 'batman', 1, 1, 1)
        user_handler.add_product('admin', 1, 1, 1)
        self.assertTrue(1 in users.get_user_by_name('admin').cart.basket_dict)
        self.assertTrue(1 in users.get_user_by_name('admin').cart.basket_dict[1].products_dict)
        self.assertTrue(1 == users.get_user_by_name('admin').cart.basket_dict[1].products_dict[1])

    def test_remove_product(self):
        self.assertRaises(Exception, user_handler.add_product, 'batman', 1, 1, 1)
        user_handler.add_product('admin', 1, 1, 1)
        self.assertTrue(1 in users.get_user_by_name('admin').cart.basket_dict)
        self.assertTrue(1 in users.get_user_by_name('admin').cart.basket_dict[1].products_dict)
        self.assertTrue(1 == users.get_user_by_name('admin').cart.basket_dict[1].products_dict[1])
        user_handler.remove_product('admin', 1, 1, 1)
        self.assertTrue(1 in users.get_user_by_name('admin').cart.basket_dict)
        self.assertFalse(1 in users.get_user_by_name('admin').cart.basket_dict[1].products_dict)

    def test_get_cart_info(self):
        self.assertTrue(len(users.get_user_by_name('admin').cart.basket_dict) == 0)
        user_handler.add_product("admin", "store", "product", 1)
        self.assertTrue(len(users.get_user_by_name('admin').cart.basket_dict) == 1)
        self.assertTrue(1 == len(user_handler.get_cart_info("admin").basket_dict))
        self.assertTrue("product" in user_handler.get_cart_info("admin").basket_dict["store"].products_dict)
        self.assertTrue(1 == user_handler.get_cart_info("admin").basket_dict["store"].products_dict["product"])
