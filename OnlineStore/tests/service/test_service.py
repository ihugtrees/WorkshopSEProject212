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
            ans_store = service.open_store("store" + str(i), "name" + str(i))[0]
            product = {
                "product_id": "product_" + str(i),
                "product_name": "product_name" + str(i),
                "quantity": i+10
            }
            service.add_new_product_to_store_inventory("user_name" + str(i), product, "store" + str(i))

            if i < 10:
                service.add_product_to_cart("user_name" + str(i), "product" + str(i), 5, "store" + str(i))

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
        ans2, user = service.get_user("user_name0")
        self.assertTrue(ans2 and (not user.is_admin))
        ans = service.login("user_name0", "0")[0]
        self.assertFalse(ans, "try to login when the user already connected")
        ans = service.login("user_name0", "1")[0]
        self.assertFalse(ans, "test: wrong password")
        ans = service.login("aaaa", "bbb")[0]
        self.assertFalse(ans, "test: bad name")

    def test_open_store(self):  # 2.5
        ans = service.open_store("store31", "user_name1")
        self.assertTrue(ans, msg="failed to open store")
        ans, store = service.get_store("store31")
        self.assertTrue(ans)
        ans = service.open_store("store31", "user_name2")
        self.assertFalse(ans, "test: store name already exist")

    def test_get_information_about_products(self):  # 2.5
        ans, info = service.get_information_about_products("store0")
        self.assertTrue(ans, "fail to open store")
        self.assertEqual(info, "TODO")

    def test_get_store(self):  # 2.5
        ans, store = service.get_store("store6")
        self.assertTrue(ans, "fail to get the store")
        self.assertEqual(store.name, "store6")

    def test_get_cart(self):
        ans, cart = service.get_cart("user_name7")
        self.assertTrue(ans)
        self.assertEqual(cart, service.get_user("user_name").user)

    def test_add_product_to_cart(self):
        ans = service.add_product_to_cart("user_name8", "product44", 5, "store8")[0]
        self.assertTrue(ans, "failed")
        self.assertTrue(service.get_user("user_name8").user.basket_dict["store8"].product_dict["product44"] == 5)

    def test_find_product_by_name(self):
        ans = service.find_product_by_name("notExist")[0]
        self.assertFalse(ans, "not exist name")
        ans, product = service.find_product_by_name("product1")
        self.assertTrue()



