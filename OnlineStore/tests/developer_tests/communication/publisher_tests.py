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
user_name0 = "user_name0"
user_name1 = "user_name1"
user_name2 = "user_name2"
user_name3 = "user_name3"


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

    def test_send_message(self):
        self.assertTrue(True)
        publisher.send_message(message="Hello mother fucker", to="user_name1", event="test event")
        user_1_msgs = users.pop_user_messages("user_name1")
        self.assertTrue(len(user_1_msgs) == 0)
        service.logout(users_hash["user_name1"])
        publisher.send_message(message="Hello mother fucker", to="user_name1", event="test event")
        user_1_msgs = users.pop_user_messages("user_name1")
        self.assertTrue(len(user_1_msgs) == 1)
        service.login("user_name1", "password1")
        user_1_msgs = users.pop_user_messages("user_name1")
        self.assertTrue(len(user_1_msgs) == 0)

    def test_send_message_to_store_employees(self):
        service.assign_store_owner(users_hash[user_name1], user_name2, "store1")
        service.assign_store_manager(users_hash[user_name1], user_name3, "store1")
        user_1_msgs = users.pop_user_messages("user_name1")
        self.assertTrue(len(user_1_msgs) == 0)
        user_2_msgs = users.pop_user_messages("user_name2")
        self.assertTrue(len(user_2_msgs) == 0)
        user_3_msgs = users.pop_user_messages("user_name3")
        self.assertTrue(len(user_3_msgs) == 0)

        service.logout(users_hash[user_name1])
        service.logout(users_hash[user_name2])
        service.logout(users_hash[user_name3])
        publisher.send_message_to_store_employees("hello employees of store1", "store1", "barzel jaja")
        user_1_msgs = users.pop_user_messages("user_name1")
        self.assertTrue(len(user_1_msgs) == 1)
        user_2_msgs = users.pop_user_messages("user_name2")
        self.assertTrue(len(user_2_msgs) == 1)
        user_3_msgs = users.pop_user_messages("user_name3")
        self.assertTrue(len(user_3_msgs) == 0)

    def test_send_remove_employee_msg(self):
        service.assign_store_owner(users_hash[user_name1], user_name2, "store1")
        service.logout(users_hash[user_name2])
        publisher.send_remove_employee_msg("i removed you stupid owner", user_name2)
        user_2_msgs = users.pop_user_messages("user_name2")
        self.assertTrue(len(user_2_msgs) == 1)

    def test_send_messages(self):
        users.add_message(user_name0,"msg1","asdjf")
        users.add_message(user_name0, "msg2", "asdjf")
        users.add_message(user_name0, "msg3", "asdjf")
        self.assertTrue(len(users.pending_messages[user_name0]) == 3)
        publisher.send_messages("user_name0")
        self.assertTrue(len(users.pop_user_messages(user_name0)) == 0)

    def test_subscribe(self):
        self.assertTrue(len(publisher.topics["store1"]) == 1)
        publisher.subscribe(user_name2, "store1")
        self.assertTrue(len(publisher.topics["store1"]) == 2)

    def test_unsubscribe(self):
        self.assertTrue(len(publisher.topics["store1"]) == 1)
        publisher.unsubscribe(user_name1, "store1")
        self.assertTrue(len(publisher.topics["store1"]) == 0)

    def test_delete_store(self):
        pass
        # topics.pop(store_name)

    def tearDown(self):
        users.users = dict()
        users.pending_messages = dict()
        users.history_messages = dict()
        purchases.purchases = dict()
        stores.store_dict = dict()
        domain_handler.auth = Authentication()
        permissions.permissions = dict()
        publisher.topics = dict()
