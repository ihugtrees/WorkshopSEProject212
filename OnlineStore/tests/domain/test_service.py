from unittest import TestCase

from OnlineStore.src.service import service


class TestService(TestCase):
    def setUp(self) -> None:
        print("test service start:")
        for i in range(0, 30):
            service.register("name" + str(i), "" + str(i))

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
        ans = service.login("user_name", "password")[0]
        self.assertTrue(ans)
        ans2, user = service.get_user("user_name_t2")
        self.assertTrue(ans2)

    def test_open_store(self):
        ans = service.register()
        ans = service.open_store("store_name_t3", "user_name_t3")

    # def test_get_information_about_products(self):
    #     ans = service.open_store("store_name_t3")[0]
    #     self.assertTrue(ans, msg="fail to open a store yamaniak")
    #     ans, info = service.get_information_about_products("store_name_t3")
