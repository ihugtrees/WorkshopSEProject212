from unittest import TestCase

from OnlineStore.src.domain.user.basket import Basket
from OnlineStore.src.domain.user.cart import Cart
from OnlineStore.src.domain.user.user import User


class TestUser(TestCase):

    def setUp(self) -> None:
        print("test user:")
        cart = Cart()
        self.user = User('admin', '123', cart, 0)

    def test_add_product_to_cart(self):
        # self.user.add_product_to_cart(1, 2)
        # expected_list = list()
        # expected_list.append(1)
        # ans = self.user.cart.basketList[2].get_product_list()
        # self.assertEqual(expected_list, ans)
        print("alive")





    def remove_product_from_cart(self):
        self.assertEqual(True, False)
        print(self.user.cart.basketList[2].get_product_list())
