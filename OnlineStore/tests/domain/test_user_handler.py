from unittest import TestCase

from OnlineStore.src.domain.user.basket import Basket
from OnlineStore.src.domain.user.cart import Cart
from OnlineStore.src.domain.user.user import User
from OnlineStore.src.domain.user.user_handler import UserHandler
from OnlineStore.src.service.service import get_into_site


class TestUserHandler(TestCase):
    def setUp(self) -> None:
        print("test user_handler:")
        self.user_handler = UserHandler()
        for i in range(0, 30):
            self.user_handler.create_user(i)
        self.user_handler.print_users()
        get_into_site()


