from unittest import TestCase

from OnlineStore.src.service import service
from OnlineStore.src.service.authentication import Authentication


class TestService(TestCase):
    def setUp(self) -> None:
        print("test service start:")
        auth = Authentication()
        product_List_for_test5 = list()
        for i in range(0, 30):
            ans = service.register("user_name" + str(i), "" + str(i))[0]
            ans_login = service.login("user_name" + str(i), str(i))[0]
            ans_store = service.open_store("store" + str(i), "user_name" + str(i))[0]
            product = {
                "product_id": "product" + str(i),
                "product_name": "product_name" + str(i),
                "quantity": i + 10
            }
            service.add_new_product_to_store_inventory("user_name" + str(i), product, "store" + str(i))

            if i < 10:
                service.logout("user_name" + str(i))
            if i < 20:
                service.add_product_to_cart("user_name" + str(i), "product" + str(i), 5, "store" + str(i))

        # for u in service.user_handler.users_dict.keys():
        # print(u)

    def test_get_into_site(self):  # 2.1
        ans, user_name = service.get_into_site()
        self.assertTrue(ans)
        ans = service.get_user(user_name)[0]
        self.assertTrue(ans)

    def test_exit_the_site(self):  # 2.2
        user_name = service.get_into_site()[1]
        ans1 = service.exit_the_site(user_name)[0]
        self.assertTrue(ans1)
        ans = service.get_user(user_name)[0]
        self.assertFalse(ans)

    def test_registered(self):  # 2.3
        ans = service.register("user_name31", "1")[0]
        if not ans:
            print("registration failed")
            self.assertTrue(ans)
        ans2, user2 = service.get_user("user_name31")
        self.assertTrue(ans2)
        self.assertTrue(user2.user_name == "user_name31")
        ans = service.register("user_name31", "1")[0]
        self.assertFalse(ans, "fail: try to register with name that already exist")

    def test_login(self):  # 2.4
        ans = service.login("user_name0", "0")[0]
        self.assertTrue(ans)
        ans2 = service.get_user("user_name0")
        self.assertTrue(ans2[0] and ans2[1].is_logged)
        ans3 = service.login("user_name0", "0")[0]
        self.assertFalse(ans3, "try to login when the user already connected")
        ans4 = service.login("user_name0", "1")[0]
        self.assertFalse(ans4, "test: wrong password")
        ans5 = service.login("aaaa", "bbb")[0]
        self.assertFalse(ans5, "test: bad name")

    def test_get_information_about_products(self):  # 2.5
        ans, info = service.get_information_about_products("store0")
        self.assertTrue(ans, "fail to get info")
        self.assertEqual(info, service.get_store("store0").inventory.products_dict, "the info is not mach")

    def test_get_store(self):  # 2.5
        ans, store = service.get_store("store6")
        self.assertTrue(ans, "fail to get the store")
        self.assertEqual(store.name, "store6")

    def test_get_cart(self):
        ans, cart = service.get_cart("user_name7")
        self.assertTrue(ans)
        self.assertEqual(cart, service.get_user("user_name7")[1].cart)

    def test_add_product_to_cart(self):  # 2.7
        store = service.get_store("store4")[1]
        product_dict = store.inventory.products_dict
        ans4 = product_dict["product4"].quantity
        #(print(ans4)) TODO why print 9???
        ans = service.add_product_to_cart("user_name11", "product4", 5, "store4")[0]
        self.assertTrue(ans, "test: add product to cart")
        self.assertTrue(service.get_user("user_name11")[1].cart.basket_dict["store4"].products_dict["product4"] == 5)
        store = service.get_store("store4")[1]
        product_dict = store.inventory.products_dict
        ans3 = product_dict["product4"].quantity
        self.assertTrue(ans3 == 4)

    def test_find_product_by_name(self):  # 2.6
        ans = service.find_product_by_name("notExist")[0]
        self.assertFalse(ans, "test: not exist name")
        ans2, product = service.find_product_by_name("product1")
        self.assertTrue(ans2 and product.quantity == 11)

    def test_get_cart_info(self):  # 2.8
        ans2 = service.add_product_to_cart("user_name15", "product6", 4, "store6")
        self.assertTrue(ans2, "test: add product to cart")
        ans, cart = service.get_cart_info("user_name15")
        self.assertTrue(ans and cart.basket_dict["store6"][0].quantity == 12)

    def test_remove_product_from_store_inventory(self):  # 2.8
        ans1 = service.find_product_by_id("product7", "store7")
        self.assertTrue(ans1[0])
        ans2 = service.remove_product_from_store_inventory("user_name7", "product7", "store7")
        self.assertTrue(ans2)
        ans3 = service.find_product_by_id("product7", "store7")
        self.assertFalse(ans3[0])

    ## TODO 2.9

    def test_logout(self):  # 3.1
        ans = service.logout("user_name12")
        self.assertTrue(ans and (not service.get_user("user_name12")[1].is_logged))

    def test_open_store(self):  # 3.2
        ans = service.open_store("store31", "user_name1")
        self.assertTrue(ans, msg="failed to open store")
        ans, store = service.get_store("store31")
        self.assertTrue(ans)
        ans = service.open_store("store31", "user_name2")
        self.assertFalse(ans, "test: store name already exist")

    def test_get_user_purchases_history(self):  # 3.7
        ans, history = service.get_user_purchases_history("user_name13")
        self.assertTrue(ans and (history == list()))
        ans2, result = service.purchase("user_name13", "TODO")
        self.assertTrue(ans2, result)
        ans3, history = service.get_user_purchases_history("user_name13")
        self.assertTrue(ans3 and (history[0] == "TODO"))

    def test_add_new_product_to_store_inventory(self):  # 4.1.1
        new_product = {
            "product_id": "product40",
            "product_name": "product_name40",
            "quantity": 40
        }
        ans = service.add_new_product_to_store_inventory("user_name14", new_product, "store14")[0]
        self.assertTrue(ans, "failed")
        self.assertTrue("product40" in service.get_store("store14")[1].inventory.products_dict)
        ans2 = service.add_new_product_to_store_inventory("user_name15", new_product, "store14")[0]
        self.assertFalse(ans2, "test: user doesnt have permissions")

    def test_remove_product_from_store_inventory(self):  # 4.1.2
        ans, result = service.remove_product_from_store_inventory("user_name14", "product15", "store15")
        self.assertFalse(ans, "test: user doesnt have permissions")
        ans, result = service.remove_product_from_store_inventory("user_name15", "product15", "store15")
        self.assertTrue(ans and (not ("product15" in service.get_store("store15")[1].inventory.products_dict)))
        ans, result = service.remove_product_from_store_inventory("user_name15", "product15", "store15")
        self.assertFalse(ans, "test: try to remove product that doesn't exist")

    def test_edit_product_details(self):  # 4.1.3
        new_description = "new description"
        ans, result = service.edit_product_details("user_name16", new_description, "store16", "product16")
        self.assertTrue(ans and (service.get_store("store16")[1].inventory.products_dict[
                                     "product16"].description == new_description))
        # ans2, error_msg = service.edit_product_details("user_name5", new_description, "store5", "product5")
        # self.assertFalse(ans2, "test: user logout")
        ans2, result2 = service.edit_product_details("user_name16", new_description, "store16", "product17")
        self.assertFalse(ans2, "test: product doesnt exist in the store")
        ans2, result2 = service.edit_product_details("user_name17", new_description, "store16", "product16")
        self.assertFalse(ans2, "test: user have no permissions")

    def test_assign_store_owner(self):  # 4.3
        ans, result = service.assign_store_owner("user_name17", "user_name18", "store17")
        self.assertTrue(ans and ("user_name18" in service.get_store("store17")[1].owners))
        ans2, result = service.assign_store_owner("user_name17", "user_name18", "store17")
        self.assertFalse(ans2, "test: try to assign owner")
        ans3, result = service.assign_store_owner("user_name18", "user_name19", "store17")
        self.assertTrue(ans3 and ("user_name19" in service.get_store("store17")[1].owners))
        ans4, result = service.assign_store_owner("user_name14", "user_name15", "store17")
        self.assertFalse(ans4, "test: no permissions to assign")

    def test_assign_store_manager(self):  # 4.3
        ans, result = service.assign_store_manager("user_name20", "user_name21", "store20")
        self.assertTrue(ans and ("user_name21" in service.get_store("store20")[1].managers))
        ans2, result = service.assign_store_manager("user_name20", "user_name21", "store20")
        self.assertFalse(ans2, "test: try to assign owner")
        ans3, result = service.assign_store_manager("user_name21", "user_name22", "store20")
        self.assertFalse(ans3, "test: 21 try to assign, he just manager")
        ans4, result = service.assign_store_manager("user_name14", "user_name15", "store17")
        self.assertFalse(ans4, "test: no permissions to assign")

    def test_edit_manager_permissions(self):  # 4.6
        pass

    def test_remove_store_manager(self):  # 4.7
        ans, result = service.assign_store_manager("user_name24", "user_name25", "store24")
        self.assertTrue(ans and ("user_name25" in service.get_store("store24")[1].managers))
        ans2, result = service.remove_store_manager("user_name24", "user_name25", "store24")
        self.assertTrue(ans2 and (not ("user_name25" in service.get_store("store24")[1].managers)))
        ans3, result = service.remove_store_manager("user_name24", "user_name25", "store24")
        self.assertFalse(ans3, "test: try to remove user that not manager")