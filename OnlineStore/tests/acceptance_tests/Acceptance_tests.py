import threading
from unittest import TestCase
import OnlineStore.src.domain_layer.domain_handler as domain_handler
from OnlineStore.src.communication_layer import publisher
from OnlineStore.src.domain_layer.store.store import Store
from OnlineStore.src.service_layer import service
from OnlineStore.src.security.authentication import Authentication
from OnlineStore.src.domain_layer.store.buying_policy_mock import BuyingPolicyMock
import OnlineStore.src.data_layer.users_data as users
import OnlineStore.src.data_layer.purchase_data as purchases
import OnlineStore.src.data_layer.permissions_data as permissions
import OnlineStore.src.data_layer.store_data as stores

product_id: int = 0
users_hash: dict = dict()


def take_info(user_name, store_name):
    cart = service.get_cart_info(user_name)[1]
    store_history = service.get_store_purchase_history(user_name, store_name)[1]
    user_history = service.get_user_purchases_history(user_name)[1]
    return cart, store_history, user_history


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
            service.register(user_name, password, 20)[0]

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

        # for u in service_layer.user_handler.users_dict.keys():
        # print(u)

    def test_get_into_site(self):  # 2.1
        ans, user_name = service.get_into_site()
        self.assertTrue(ans)
        try:
            users.get_user_by_name(user_name)
        except Exception as e:
            self.fail(e.args[0])

    def test_exit_the_site(self):  # 2.2
        user_name = service.get_into_site()[1]
        ans1 = service.exit_the_site(user_name)[0]
        self.assertTrue(ans1)
        with self.assertRaises(Exception):
            users.get_user_by_name(user_name)

    def test_registered(self):  # 2.3
        user_name = "user_name10000"
        password = "1"

        ans = service.register(user_name, password, 20)
        self.assertTrue(ans[0], ans[1])
        service.login(user_name, password)[1]

        try:
            user2 = users.get_user_by_name(user_name)
        except Exception as e:
            self.fail(e.args[0])
        self.assertTrue(user2.user_name == "user_name10000")

        ans = service.register("user_name10000", password, 20)
        self.assertFalse(ans[0], ans[1])

    def test_login(self):  # 2.4
        user_name = "user_name0"
        password = "password0"

        ans = service.login(user_name, password)
        self.assertTrue(ans[0], ans[1])

        try:
            # ans2 = users.get_user_by_name(user_name)
            # self.assertTrue(ans2.is_logged)
            self.assertTrue(domain_handler.auth.authenticate_session(ans[1]) == None)
        except Exception as e:
            self.fail(e.args[0])

        ans3 = service.login(user_name, password)
        self.assertFalse(ans3[0], ans3[1])

        ans4 = service.login(user_name, "wrong password")[0]
        self.assertFalse(ans4, "test: wrong password")

        ans5 = service.login("aaaa", "bbb")[0]
        self.assertFalse(ans5, "test: bad name")

    # def test_test_login_sync(self):
    #     t1 = threading.Thread(service_layer.login, ("user_name5", "5",))
    #     t2 = threading.Thread(service_layer.login, ("user_name5", "5"))

    def test_get_information_about_products(self):  # 2.5
        store_name = "store0"
        ans, info = service.get_information_about_products(store_name)
        self.assertTrue(ans, "fail to get info")
        self.assertEqual(info, service.get_store_for_tests(store_name)[1].inventory.products_dict,
                         "the info is not mach")

    def test_get_store(self):  # 2.5
        store_name = "store0"
        ans = service.get_store_info(store_name)
        self.assertTrue(ans[0], ans[1])
        self.assertEqual(ans[1]["Store name:"], store_name)
        # {"store_name": store.name, "store_founder": store.store_founder,
        #  "buying_policy": store.buying_policy, "discount_policy": store.discount_policy}

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
        ans = service.search_product_by_id(product_name)
        self.assertTrue(ans[0], ans[1])
        quantity = ans[1].quantity
        self.assertTrue(quantity == 10, quantity)

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
        ans2, result = service.search_product_by_name("product", filters)
        self.assertTrue(ans2 and result[0].quantity == 10, result)

    def test_search_product_by_keyword(self):  # 2.6.3
        filters = {'min': 0, 'max': 500, 'prating': 0, 'category': '', 'srating': 0}
        ans = service.search_product_by_keyword("not exist", filters)
        self.assertFalse(ans[0], ans[1])
        ans = service.search_product_by_name("", filters)
        self.assertTrue(ans[0] and ans[1][0].quantity == 10)

    def test_add_product_to_cart(self):  # 2.7
        store_name = "store1"
        product_name = "product"
        user_name = "user_name1"
        user_name_hash = users_hash[user_name]

        store = service.get_store_for_tests(store_name)[1]
        product_dict = store.inventory.products_dict
        ans4 = product_dict[product_name].quantity
        self.assertTrue(ans4 == 10)

        ans = service.add_product_to_cart(user_name_hash, product_name, 5, store_name)[0]
        self.assertTrue(ans, "test: add product to cart")
        try:
            user = users.get_user_by_name(user_name)
        except Exception as e:
            self.fail(e.args[0])
        self.assertTrue(
            user.cart.basket_dict[store_name].products_dict[product_name] == 10)
        store = service.get_store_for_tests(store_name)[1]
        product_dict = store.inventory.products_dict
        ans3 = product_dict[product_name].quantity
        self.assertTrue(ans3 == 10)

    def test_get_cart_info(self):  # 2.8
        user_name = users_hash["user_name2"]
        product_name = "product"
        store_name = "store1"

        ans2 = service.add_product_to_cart(user_name, product_name, 4, store_name)
        self.assertTrue(ans2[0], ans2[1])

        ans, cart = service.get_cart_info(user_name)
        self.assertTrue(ans and cart.basket_dict[store_name].products_dict[product_name] == 4, cart)

    def test_remove_product_from_store_inventory(self):  # 4.1.2
        store_name = "store1"
        product_name = "product"
        user_name = users_hash["user_name1"]

        ans = service.find_product_by_id(product_name, store_name)
        self.assertTrue(ans[0], ans[1])

        ans = service.remove_product_from_store_inventory(user_name, product_name, store_name)
        self.assertTrue(ans[0], ans[1])

        ans = service.find_product_by_id(product_name, store_name)
        self.assertFalse(ans[0], ans[1])

    # 2.9.0
    def test_purchase(self):
        user_name = users_hash["user_name1"]
        store_name = "store1"
        product_name = "product"

        cart_before, store_history_before, user_history_before = take_info(user_name, store_name)

        ans = service.purchase(user_name, {"card_number": "123123"}, "Ziso 5/3, Beer Sheva")

        cart_after, store_history_after, user_history_after = take_info(user_name, store_name)

        self.assertTrue(ans[0], ans[1])
        store: Store = service.get_store_for_tests(store_name)[1]
        quantity = store.inventory.products_dict.get(product_name).quantity

        self.assertTrue(
            (quantity == 5),
            "quntity didnt drop")

        service.add_product_to_cart(user_name, product_name, 50, store_name)

        cart_before, store_history_before, user_history_before = take_info(user_name, store_name)

        ans = service.purchase(user_name, {"card_number": "123123"}, "Ziso 5/3, Beer Sheva")

        cart_after, store_history_after, user_history_after = take_info(user_name, store_name)

        self.assertTrue(ans[0] == False and ans[1].find("There are only") >= 0, ans[1])
        self.assertTrue((service.get_store_for_tests(store_name)[1].inventory.products_dict.get(product_name).quantity
                         == 5), "quantity drop")
        for store_name, basket in cart_before.basket_dict.items():
            self.assertDictEqual(basket.products_dict, cart_after.basket_dict[store_name].products_dict)
        self.assertTrue(len(store_history_before) == len(store_history_after))
        self.assertTrue(len(user_history_before) == len(user_history_after))

    def test_purchase_delivery_fail(self):
        user_name = users_hash["user_name1"]
        store_name = "store1"
        product_name = "product"

        cart_before, store_history_before, user_history_before = take_info(user_name, store_name)

        ans = service.purchase(user_name, {"card_number": "123"}, "haifa")

        cart_after, store_history_after, user_history_after = take_info(user_name, store_name)

        self.assertTrue(ans[0] == False and ans[1] == "Delivery system rejected the delivery", ans[1])
        self.assertTrue((service.get_store_for_tests(store_name)[1].inventory.products_dict.get(product_name).quantity
                         == 10), "quantity drop")

        for store_name, basket in cart_before.basket_dict.items():
            self.assertDictEqual(basket.products_dict, cart_after.basket_dict[store_name].products_dict)
        self.assertTrue(len(store_history_before) == len(store_history_after))
        self.assertTrue(len(user_history_before) == len(user_history_after))

        cart_before, store_history_before, user_history_before = take_info(user_name, store_name)

        for store_name, basket in cart_before.basket_dict.items():
            self.assertDictEqual(basket.products_dict, cart_after.basket_dict[store_name].products_dict)
        self.assertTrue(len(store_history_before) == len(store_history_after))
        self.assertTrue(len(user_history_before) == len(user_history_after))

    def test_purchase_payment_fail(self):
        user_name = users_hash["user_name1"]
        store_name = "store1"
        product_name = "product"

        cart_before, store_history_before, user_history_before = take_info(user_name, store_name)

        ans = service.purchase(user_name, {"card_number": "0000"}, "Tel Aviv")

        cart_after, store_history_after, user_history_after = take_info(user_name, store_name)

        self.assertTrue(ans[0] == False and ans[1] == "Payment system rejected the card", ans[1])
        self.assertTrue((service.get_store_for_tests(store_name)[1].inventory.products_dict.get(product_name).quantity
                         == 10), "quantity drop")

        for store_name, basket in cart_before.basket_dict.items():
            self.assertDictEqual(basket.products_dict, cart_after.basket_dict[store_name].products_dict)
        self.assertTrue(len(store_history_before) == len(store_history_after))
        self.assertTrue(len(user_history_before) == len(user_history_after))

        for store_name, basket in cart_before.basket_dict.items():
            self.assertDictEqual(basket.products_dict, cart_after.basket_dict[store_name].products_dict)
        self.assertTrue(len(store_history_before) == len(store_history_after))
        self.assertTrue(len(user_history_before) == len(user_history_after))

    def test_purchase_buying_policy_fail(self):
        user_name = users_hash["user_name9"]
        store_name = "store9"
        product_name = "product"
        service.get_store_for_tests(store_name)[1].buying_policy = BuyingPolicyMock()

        anst = service.add_product_to_cart(user_name, product_name, 1, store_name)
        #self.assertTrue(anst[0], anst[1])
        cart_before, store_history_before, user_history_before = take_info(user_name, store_name)

        ans = service.purchase(user_name, {"card_number": "312312"}, "Noga Hakalanit 26")

        cart_after, store_history_after, user_history_after = take_info(user_name, store_name)

        self.assertTrue(((ans[0] == False) and (ans[1] == "buying policy fails")), ans[1])
        self.assertTrue((service.get_store_for_tests(store_name)[1].inventory.products_dict.get(product_name).quantity
                         == 10), "quantity drop")
        for store_name, basket in cart_before.basket_dict.items():
            self.assertDictEqual(basket.products_dict, cart_after.basket_dict[store_name].products_dict)
        self.assertTrue(len(store_history_before) == len(store_history_after))
        self.assertTrue(len(user_history_before) == len(user_history_after))

    def test_purchase_sync(self):
        user_name0 = users_hash["user_name4"]
        user_name1 = users_hash["user_name1"]
        user_name2 = users_hash["user_name2"]
        user_name3 = users_hash["user_name3"]
        store_name = "store4"
        product_name = "product"
        add_to_cart1 = service.add_product_to_cart(user_name1, product_name, 5, store_name)
        self.assertTrue(add_to_cart1[0], add_to_cart1[1])
        service.add_product_to_cart(user_name2, product_name, 5, store_name)
        service.add_product_to_cart(user_name3, product_name, 5, store_name)

        t1 = threading.Thread(target=service.purchase,
                              args=(user_name0, {"card_number": "1234"}, "Ziso 5/3, Beer Sheva",))
        t2 = threading.Thread(target=service.purchase,
                              args=(user_name1, {"card_number": "1234"}, "Ziso 5/3, Beer Sheva",))
        t3 = threading.Thread(target=service.purchase,
                              args=(user_name2, {"card_number": "1234"}, "Ziso 5/3, Beer Sheva",))
        t4 = threading.Thread(target=service.purchase,
                              args=(user_name3, {"card_number": "1234"}, "Ziso 5/3, Beer Sheva",))
        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        store = service.get_store_for_tests(store_name)[1]
        quantity = store.inventory.products_dict[product_name].quantity

        self.assertTrue(quantity == 0)
        ans, store_history = service.get_store_purchase_history(user_name0, store_name)
        self.assertTrue(ans, store_history)
        self.assertTrue(len(store_history) == 2, str(len(store_history)))

    def test_logout(self):  # 3.1
        user_name = "user_name1"
        user_name_hash = users_hash[user_name]
        service.login(user_name, "password1")
        ans = service.logout(user_name_hash)
        try:
            user = users.get_user_by_name(user_name)
        except Exception as e:
            self.assertTrue(False, e.args[0])
        self.assertTrue(ans[0])
        with self.assertRaises(Exception):
            domain_handler.auth.authenticate_session(ans[1])

        # not logged in
        user_name = "user_name0"
        user_name_hash = users_hash[user_name]
        ans = service.logout(user_name_hash)
        self.assertFalse(ans[0], "Not logged in called log out and succeeded")

    def test_open_store(self):  # 3.2
        store_name = "new store"
        user_name = users_hash["user_name1"]

        ans = service.open_store(store_name, user_name)
        self.assertTrue(ans[0], msg=ans[1])

        ans, store = service.get_store_for_tests(store_name)
        self.assertTrue(ans)
        ans = service.open_store(store_name, user_name)
        self.assertFalse(ans[0], ans[1])

    def test_get_user_purchases_history(self):  # 3.7
        user_name = users_hash["user_name1"]

        ans = service.get_user_purchases_history(user_name)
        self.assertTrue(ans[0] and (len(ans[1]) == 0), ans[1])

        ans = service.purchase(user_name, {"card_number": 1}, "Beer Sheva")
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
        self.assertTrue(new_product_name in service.get_store_for_tests(store_name)[1].inventory.products_dict)

        wrong_user_name = users_hash["user_name0"]
        ans2 = service.add_new_product_to_store_inventory(wrong_user_name, new_product, store_name)[0]
        self.assertFalse(ans2, "test: user doesnt have permissions")

    def test_edit_product_details(self):  # 4.1.3
        store_name = "store1"
        user_name = users_hash["user_name1"]
        product_name = "product"
        new_description = "new description"

        ans = service.edit_product_description(user_name, new_description, store_name, product_name)
        self.assertTrue(ans[0] and (service.get_store_for_tests(store_name)[1].inventory.products_dict[
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

        ans = service.assign_store_owner(user_name, assignee_user_name, store_name)
        self.assertTrue(ans[0], ans[1])

        ans = service.assign_store_owner(user_name, assignee_user_name, store_name)
        self.assertFalse(ans[0], ans[1])

        not_owner_already_name = users_hash["user_name0"]
        ans = service.assign_store_owner(not_owner_already_name, users_hash["user_name4"], store_name)
        self.assertFalse(ans[0], ans[1])

        not_owner_already_name = "user_name0"
        assignee_user_name = users_hash["user_name2"]
        ans = service.assign_store_owner(assignee_user_name, not_owner_already_name, store_name)
        self.assertTrue(ans[0], ans[1])

    def test_add_discount(self):  # 4.2
        user_name = users_hash["user_name1"]
        store_name = "store1"
        service.add_term_discount(user_name, store_name, "d1", "milk 20", "milk quantity > 50")
        self.assertTrue(len(service.get_store_for_tests(store_name)[1].discount_policy.discount_dict) == 1)

    def test_add_buying_policy(self):  # 4.2
        user_name = users_hash["user_name1"]
        store_name = "store1"
        service.add_buying_policy(user_name, store_name, "p1", "milk quantity > 50")
        self.assertTrue(len(service.get_store_for_tests(store_name)[1].buying_policy.terms_dict) == 1)

    def test_assign_store_manager(self):  # 4.3
        user_name = users_hash["user_name1"]
        new_store_manager_name = "user_name2"
        store_name = "store1"

        ans, result = service.assign_store_manager(user_name, new_store_manager_name, store_name)
        self.assertTrue(ans, result)

        ans2, result = service.assign_store_manager(user_name, new_store_manager_name, store_name)
        self.assertFalse(ans2, result)

        not_user_manager = "user_name3"
        ans3, result = service.assign_store_manager(new_store_manager_name, not_user_manager, store_name)
        self.assertFalse(ans3, result)

        not_user_manager = users_hash["user_name3"]
        ans4, result = service.assign_store_manager(not_user_manager, "user_name4", store_name)
        self.assertFalse(ans4, result)

    def test_assign_store_manager_sync(self):
        user_name0 = users_hash["user_name0"]
        user_name1 = users_hash["user_name1"]
        user_name2 = users_hash["user_name2"]
        user_name3 = users_hash["user_name3"]
        store_name = "store0"
        product_name = "product"
        store_before: Store = service.get_store_for_tests(store_name)[1]
        # assign_list = store_before.managers
        # self.assertTrue(len(assign_list) == 0) TODO
        t1 = threading.Thread(target=service.assign_store_manager,
                              args=(user_name0, user_name3, store_name,))
        t2 = threading.Thread(target=service.assign_store_manager,
                              args=(user_name1, user_name3, store_name,))
        t3 = threading.Thread(target=service.assign_store_manager,
                              args=(user_name2, user_name3, store_name,))
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
        store: Store = service.get_store_for_tests(store_name)[1]
        # assign_list = store.managers
        # self.assertTrue(len(assign_list) == 1)

    def test_edit_manager_permissions(self):  # 4.6
        pass

    def test_remove_store_owner(self):  # 4.4
        user_name = users_hash["user_name1"]
        store_name = "store1"
        removed_manager = "user_name2"

        ans, result = service.assign_store_owner(user_name, removed_manager, store_name)
        self.assertTrue(ans, result)

        ans, result = service.assign_store_owner(users_hash[removed_manager], "user_name3", store_name)
        self.assertTrue(ans, result)

        ans, result = service.assign_store_owner(users_hash["user_name3"], "user_name4", store_name)
        self.assertTrue(ans, result)

        ans2, result = service.remove_store_owner(user_name, removed_manager, store_name)
        self.assertTrue(ans2, result)

        ans3, result = service.remove_store_owner(user_name, removed_manager, store_name)
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

        ans = service.purchase(user_name, {"card_number": 1}, "Beer Sheva")
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
            t1 = threading.Thread(target=service.register, args=("user_name33", "33", 23,))
            t2 = threading.Thread(target=service.register, args=("user_name33", "33", 23,))
            t3 = threading.Thread(target=service.register, args=("user_name33", "33", 23,))
            t4 = threading.Thread(target=service.register, args=("user_name33", "33", 23,))
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

    def test_real_time_notifications(self):  # 9.1
        user_name0 = "user_name0"
        user_name1 = "user_name1"
        user_name2 = "user_name2"
        user_name3 = "user_name3"
        service.assign_store_owner(users_hash[user_name1],user_name2,"store1")
        service.assign_store_owner(users_hash[user_name1], user_name3, "store1")
        self.assertTrue(len(publisher.topics["store1"]) == 3)
        service.add_product_to_cart(users_hash["user_name4"], "product", 1, "store1")
        service.purchase(users_hash["user_name4"], {"card_number": 1}, "Beer Sheva")
        self.assertTrue(len(users.history_messages[user_name1]) == 1, f"len(list) of {user_name1} should be 1")
        self.assertTrue(len(users.history_messages[user_name2]) == 1, f"len(list) of {user_name2} should be 1")
        self.assertTrue(len(users.history_messages[user_name3]) == 1, f"len(list) of {user_name3} should be 1")

        service.logout(users_hash[user_name1])
        service.logout(users_hash[user_name2])
        service.logout(users_hash[user_name3])

        service.add_product_to_cart(users_hash["user_name4"], "product", 1, "store1")
        service.purchase(users_hash["user_name4"], {"card_number": 1}, "Beer Sheva")

        self.assertTrue(len(users.pending_messages[user_name1]) == 1, f"len(list) of {user_name1} should be 1")
        self.assertTrue(len(users.pending_messages[user_name2]) == 1, f"len(list) of {user_name2} should be 1")
        self.assertTrue(len(users.pending_messages[user_name3]) == 1, f"len(list) of {user_name3} should be 1")

        service.login(user_name1, "password1")
        service.remove_store_owner(users_hash[user_name1], user_name2, "store1")
        self.assertTrue(len(users.pending_messages[user_name2]) == 2, f"len(list) of {user_name2} should be 1")


    def tearDown(self):
        users.users = dict()
        users.pending_messages = dict()
        users.history_messages = dict()
        purchases.purchases = dict()
        stores.store_dict = dict()
        domain_handler.auth = Authentication()
        permissions.permissions = dict()
        publisher.topics = dict()

