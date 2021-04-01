from unittest import TestCase

from OnlineStore.src.domain.user.user import User


class TestUser(TestCase):
    def setUp(self) -> None:
        self.user = User()

    def test_view_cart(self):
        pass
