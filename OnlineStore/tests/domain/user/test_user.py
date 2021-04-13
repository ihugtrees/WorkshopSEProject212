from unittest import TestCase

from OnlineStore.src.domain.user.cart import Cart
from OnlineStore.src.domain.user.user import User


class TestUser(TestCase):
    def setUp(self):
        cart = Cart()
        self.user = User('admin', cart, True)

    def test_add_product_to_cart(self):
        self.user.add_product_to_user(1, 2)
        expected_list = list()
        expected_list.append(1)
        ans = self.user.cart.basketList[2].get_product_dict()
        self.assertEqual(expected_list, ans)
        print("alive")

    def test_remove_product_from_cart(self):
        self.assertEqual(True, False)
        print(self.user.cart.basketList[2].get_product_dict())
