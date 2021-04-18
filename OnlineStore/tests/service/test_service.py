import threading
from unittest import TestCase

from OnlineStore.src.service import service
from OnlineStore.src.security.authentication import Authentication
import OnlineStore.src.data_layer.users_data as users
import OnlineStore.src.data_layer.purchase_data as purchases

product_id: int = 0
users_hash: dict = dict()


class TestService(TestCase):
    def setUp(self):
        global product_id
        global users_hash
        product_id = 0

        for i in range(0, 10):
            service.get_into_site()
            user_name = "user_name" + str(i)
            password = "password" + str(i)
            store_name = "store" + str(i)
            service.register(user_name, password)[0]

            user_name_hash = service.login(user_name, password)[1]
            users_hash[user_name] = user_name_hash

            service.open_store(store_name, user_name_hash)[0]
            product = {
                "product_id": "product",
                "product_name": "product",
                "quantity": 10,
                "price": 10
            }
            service.add_new_product_to_store_inventory(user_name_hash, product, store_name)

            service.add_product_to_cart(user_name_hash, "product", 5, store_name)

            product_id += 1

        service.logout(users_hash["user_name0"])

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
        user_name = "user_name10000"
        password = "1"

        ans = service.register(user_name, password)
        self.assertTrue(ans[0], ans[1])
        user_name = service.login(user_name, password)[1]

        ans2, user2 = service.get_user(user_name)
        self.assertTrue(ans2, user2)
        self.assertTrue(user2.user_name == "user_name10000")

        ans = service.register("user_name10000", password)
        self.assertFalse(ans[0], ans[1])

    def test_login(self):  # 2.4
        user_name = "user_name0"
        password = "password0"

        ans = service.login(user_name, password)
        user_name = ans[1]
        self.assertTrue(ans[0], ans[1])

        ans2 = service.get_user(user_name)
        self.assertTrue(ans2[0] and ans2[1].is_logged)

        ans3 = service.login(user_name, password)[0]
        self.assertFalse(ans3, "try to login when the user already connected")

        ans4 = service.login(user_name, "wrong password")[0]
        self.assertFalse(ans4, "test: wrong password")

        ans5 = service.login("aaaa", "bbb")[0]
        self.assertFalse(ans5, "test: bad name")

    # def test_test_login_sync(self):
    #     t1 = threading.Thread(service.login, ("user_name5", "5",))
    #     t2 = threading.Thread(service.login, ("user_name5", "5"))

    def test_get_information_about_products(self):  # 2.5
        store_name = "store0"
        ans, info = service.get_information_about_products(store_name)
        self.assertTrue(ans, "fail to get info")
        self.assertEqual(info, service.get_store(store_name)[1].inventory.products_dict, "the info is not mach")

    def test_get_store(self):  # 2.5
        store_name = "store0"
        ans, store = service.get_store(store_name)
        self.assertTrue(ans, "fail to get the store")
        self.assertEqual(store.name, store_name)

    def test_get_cart(self):
        user_name = users_hash["user_name0"]
        ans, cart = service.get_cart(user_name)
        self.assertTrue(ans)
        self.assertEqual(cart, service.get_user(user_name)[1].cart)

    def test_find_product_by_id(self):  # 2.6
        store_name = "store0"
        product_name = "product"
        ans = service.find_product_by_id("notExist", store_name)[0]
        self.assertFalse(ans, "test: not exist name")
        ans2, product = service.find_product_by_id(product_name, store_name)
        self.assertTrue(ans2 and product.quantity == 10)

    def test_search_product_by_id(self):  # 2.6.0
        product_name = "product"
        ans = service.search_product_by_id("notExist")[0]
        self.assertFalse(ans, "test: not exist name")
        ans2, product = service.search_product_by_id(product_name)
        quantity = product.quantity
        self.assertTrue(ans2 and quantity == 10)

    def test_search_product_by_category(self):  # 2.6.1
        filters = {'min': 0, 'max': 500, 'prating': 0, 'category': '', 'srating': 0}
        ans = service.search_product_by_category("dogs", filters)
        self.assertFalse(ans[0], ans[1])
        ans2, product_list = service.search_product_by_category("null", filters)
        self.assertTrue(ans2 and (len(product_list) == product_id), product_list)

    def test_search_product_by_name(self):  # 2.6.2
        filters = {'min': 0, 'max': 500, 'prating': 0, 'category': '', 'srating': 0}
        ans, result = service.search_product_by_name("not exist", filters)
        self.assertFalse(ans)
        ans2, result = service.search_product_by_name("product" , filters)
        self.assertTrue(ans2 and result[0].quantity == 10)

    def test_search_product_by_keyword(self):  # 2.6.3
        filters = {'min': 0, 'max': 500, 'prating': 0, 'category': '', 'srating': 0}
        ans, result = service.search_product_by_keyword("not exist", filters)
        self.assertFalse(ans)
        ans2, result = service.search_product_by_name("", filters)
        self.assertTrue(ans2 and result[0].quantity == 10)

    def test_add_product_to_cart(self):  # 2.7
        store_name = "store0"
        product_name = "product"
        user_name = users_hash["user_name0"]

        store = service.get_store(store_name)[1]
        product_dict = store.inventory.products_dict
        ans4 = product_dict[product_name].quantity
        self.assertTrue(ans4 == 10)

        ans = service.add_product_to_cart(user_name, product_name, 5, store_name)[0]
        self.assertTrue(ans, "test: add product to cart")
        self.assertTrue(service.get_user(user_name)[1].cart.basket_dict[store_name].products_dict[product_name] == 10)
        store = service.get_store(store_name)[1]
        product_dict = store.inventory.products_dict
        ans3 = product_dict[product_name].quantity
        self.assertTrue(ans3 == 10)

    def test_get_cart_info(self):  # 2.8
        user_name = users_hash["user_name0"]
        product_name = "product"
        store_name = "store1"

        ans2 = service.add_product_to_cart(user_name, product_name, 4, store_name)
        self.assertTrue(ans2[0], ans2[1])

        ans, cart = service.get_cart_info(user_name)
        self.assertTrue(ans and cart.basket_dict[store_name].products_dict[product_name] == 4, cart)

    def test_remove_product_from_store_inventory(self):  # 4.1.2
        store_name = "store0"
        product_name = "product"
        user_name = users_hash["user_name0"]

        ans1 = service.find_product_by_id(product_name, store_name)
        self.assertTrue(ans1[0])

        ans2 = service.remove_product_from_store_inventory(user_name, product_name, store_name)
        self.assertTrue(ans2)

        ans3 = service.find_product_by_id(product_name, store_name)
        self.assertFalse(ans3[0])

    # 2.9.0
    def test_purchase(self):
        user_name = users_hash["user_name0"]
        store_name = "store0"
        product_name = "product"

        ans = service.purchase(user_name, {}, "Ziso 5/3, Beer Sheva")
        self.assertTrue(ans[0], ans[1])
        self.assertTrue((service.get_store(store_name)[1].inventory.products_dict.get(product_name).quantity == 5),
                        "quntity didnt drop")

        service.add_product_to_cart(user_name, product_name, 50, store_name)
        ans = service.purchase(user_name, {}, "Ziso 5/3, Beer Sheva")
        self.assertFalse(ans[0], ans[1])

    def test_logout(self):  # 3.1
        user_name = users_hash["user_name1"]
        ans = service.logout(user_name)
        self.assertTrue(ans and (not service.get_user(user_name)[1].is_logged))

    def test_open_store(self):  # 3.2
        store_name = "new store"
        user_name = users_hash["user_name1"]

        ans = service.open_store(store_name, user_name)[0]
        self.assertTrue(ans, msg="failed to open store")

        ans, store = service.get_store(store_name)
        self.assertTrue(ans)
        ans = service.open_store(store_name, user_name)[0]
        self.assertFalse(ans, "test: store name already exist")

    def test_get_user_purchases_history(self):  # 3.7
        user_name = users_hash["user_name1"]

        ans = service.get_user_purchases_history(user_name)
        self.assertTrue(ans[0] and (len(ans[1]) == 0), ans[1])

        ans = service.purchase(user_name, {"TODO": 1}, "Beer Sheva")
        self.assertTrue(ans[0], ans[1])

        ans = service.get_user_purchases_history(user_name)
        self.assertTrue(ans[0] and (len(ans[1]) == 1), ans[1])

    def test_add_new_product_to_store_inventory(self):  # 4.1.1
        new_product_name = "new product"
        store_name = "store1"
        user_name = users_hash["user_name1"]
        new_product = {
            "product_id": new_product_name,
            "product_name": new_product_name,
            "quantity": 40,
            "price": 10
        }
        ans = service.add_new_product_to_store_inventory(user_name, new_product, store_name)
        self.assertTrue(ans[0], ans[1])
        self.assertTrue(new_product_name in service.get_store(store_name)[1].inventory.products_dict)

        wrong_user_name = users_hash["user_name0"]
        ans2 = service.add_new_product_to_store_inventory(wrong_user_name, new_product, store_name)[0]
        self.assertFalse(ans2, "test: user doesnt have permissions")

    def test_edit_product_details(self):  # 4.1.3
        store_name = "store1"
        user_name = users_hash["user_name1"]
        product_name = "product"
        new_description = "new description"

        ans = service.edit_product_description(user_name, new_description, store_name, product_name)
        self.assertTrue(ans[0] and (service.get_store(store_name)[1].inventory.products_dict[
                                        product_name].description == new_description), ans[1])

        ans = service.edit_product_description(user_name, new_description, store_name, "product17")
        self.assertFalse(ans[0], ans[1])

        wrong_user_name = users_hash["user_name0"]
        ans = service.edit_product_description(wrong_user_name, new_description, store_name, product_name)
        self.assertFalse(ans[0], ans[1])

    def test_assign_store_owner(self):  # 4.3
        user_name = users_hash["user_name1"]
        assignee_user_name = "user_name2"
        store_name = "store1"
        service.login("user_name0", "password0")

        ans, result = service.assign_store_owner(user_name, assignee_user_name, store_name)
        self.assertTrue(ans and (assignee_user_name in service.get_store(store_name)[1].owners))

        ans2, result = service.assign_store_owner(user_name, assignee_user_name, store_name)
        self.assertFalse(ans2, result)

        not_owner_already_name = users_hash["user_name0"]
        ans4, result = service.assign_store_owner(not_owner_already_name, users_hash["user_name4"], store_name)
        self.assertFalse(ans4, result)

        not_owner_already_name = "user_name0"
        assignee_user_name = users_hash["user_name2"]
        ans3, result = service.assign_store_owner(assignee_user_name, not_owner_already_name, store_name)
        self.assertTrue(ans3 and (not_owner_already_name in service.get_store(store_name)[1].owners), result)

    def test_assign_store_manager(self):  # 4.3
        user_name = users_hash["user_name1"]
        new_store_manager_name = "user_name2"
        store_name = "store1"

        ans, result = service.assign_store_manager(user_name, new_store_manager_name, store_name)
        self.assertTrue(ans and (new_store_manager_name in service.get_store(store_name)[1].managers))

        ans2, result = service.assign_store_manager(user_name, new_store_manager_name, store_name)
        self.assertFalse(ans2, result)

        not_user_manager = "user_name3"
        ans3, result = service.assign_store_manager(new_store_manager_name, not_user_manager, store_name)
        self.assertFalse(ans3, result)

        not_user_manager = users_hash["user_name3"]
        ans4, result = service.assign_store_manager(not_user_manager, "user_name4", store_name)
        self.assertFalse(ans4, result)

    def test_edit_manager_permissions(self):  # 4.6
        pass

    def test_remove_store_manager(self):  # 4.7
        user_name = users_hash["user_name1"]
        store_name = "store1"
        removed_manager = "user_name2"

        ans, result = service.assign_store_manager(user_name, removed_manager, store_name)
        self.assertTrue(ans and (removed_manager in service.get_store(store_name)[1].managers), result)

        ans2, result = service.remove_store_manager(user_name, removed_manager, store_name)
        self.assertTrue(ans2 and (not (removed_manager in service.get_store(store_name)[1].managers)), result)

        ans3, result = service.remove_store_manager(user_name, removed_manager, store_name)
        self.assertFalse(ans3, result)

    def test_get_employee_information(self):  # 4.9.1
        user_name = users_hash["user_name1"]
        store_name = "store1"
        new_store_manager = "user_name2"

        ans, result = service.assign_store_manager(user_name, new_store_manager, store_name)
        self.assertTrue(ans, result)

        ans = service.get_employee_information(user_name, new_store_manager, store_name)
        self.assertTrue(ans[0], ans[1])

        not_an_employee = "user_name3"
        ans = service.get_employee_information(user_name, not_an_employee, store_name)
        self.assertFalse(ans[0], ans[1])

    def test_get_store_purchase_history(self):  # 4.11 TODO not thorough enough
        user_name = users_hash["user_name1"]
        store_name = "store1"

        ans = service.purchase(user_name, {"payment info TODO": 1}, "Beer Sheva")
        self.assertTrue(ans[0], ans[1])

        ans = service.get_store_purchase_history(user_name, store_name)
        self.assertTrue(ans[0], ans[1])

    def test_get_store_purchase_history_admin(self):  # 6.4.1
        pass

    def test_get_into_site_sync(self):
        try:
            num_of_users = len(users.users)
            t1 = threading.Thread(target=service.get_into_site, args=())
            t2 = threading.Thread(target=service.get_into_site, args=())
            t3 = threading.Thread(target=service.get_into_site, args=())
            t4 = threading.Thread(target=service.get_into_site, args=())
            t1.start()
            t2.start()
            t3.start()
            t4.start()

            t1.join()
            t2.join()
            t3.join()
            t4.join()
            num_after = len(users.users)
            bool = num_of_users + 4 == num_after
            self.assertTrue(bool)
        except:
            self.assertTrue(False, "bug")

    def test_register_sync(self):
        try:
            t1 = threading.Thread(target=service.register, args=("user_name33", "33",))
            t2 = threading.Thread(target=service.register, args=("user_name33", "33",))
            t3 = threading.Thread(target=service.register, args=("user_name33", "33",))
            t4 = threading.Thread(target=service.register, args=("user_name33", "33",))
            t1.start()
            t2.start()
            t3.start()
            t4.start()

            t1.join()
            t2.join()
            t3.join()
            t4.join()

        except:
            self.assertTrue(False, "buuug")

    def tearDown(self):
        users.users = dict()
        purchases.purchases = dict()
        service.store_handler.store_dict = dict()
        service.auth = Authentication()
