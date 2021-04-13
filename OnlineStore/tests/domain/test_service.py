from unittest import TestCase

from OnlineStore.src.service import service


class TestService(TestCase):
    def setUp(self) -> None:
        print("test service start:")
        product_List_for_test5 = list()
        for i in range(0, 30):
            service.register("name" + str(i), "" + str(i))
            service.open_store("store" + str(i), "name"+ str(i))
            for j in range(0, 3):
                service.add_product("name" + str(i), "product"+str(j), 5, "store" + str(i))

    def test_registered(self):
        ans = service.register("user_name_t1", "password")[0]
        if not ans:
            print("registration failed")
            self.assertTrue(ans)

        ans2, user2 = service.get_user("user_name")
        self.assertTrue(ans2)
        if user2.user_name == "user_name_t1" and user2.password == "password":
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_login(self):
        ans = service.login("user_name0", "0")[0]
        self.assertTrue(ans)
        ans2, user = service.get_user("user_name0")
        self.assertTrue(ans2)

    def test_open_store(self):
        ans = service.open_store("store31", "user_name1")
        self.assertTrue(ans, msg = "failed to open store")
        ans, store = service.get_store("store31")
        self.assertTrue(ans)

    def test_get_information_about_products(self):
        ans, info = service.get_information_about_products("store0")
        self.assertTrue(ans, "fail to open store")
        self.assertEqual(info, "TODO")


