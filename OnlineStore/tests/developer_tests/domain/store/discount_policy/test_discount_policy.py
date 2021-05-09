from unittest import TestCase

from OnlineStore.src.domain.store.discont_policy.atomic_term import AtomicTerm
from OnlineStore.src.domain.store.discont_policy.discount_policy import DiscountPolicy
from OnlineStore.src.domain.store.discont_policy.term_discount import TermDiscount
from OnlineStore.src.domain.store.store import Store


class TestDiscountPolicy(TestCase):
    def setUp(self):
        self.basketDTO = basketDTO = {
            "milk": (20, 20, "milk"),  # key - product name value - (quantity, price)
            "yogurt": (50, 10, "milk"),
            "avocado": (32, 4, "veg")
        }
        self.discount_policy = DiscountPolicy()


    def test_add_discount(self):
        self.discount_policy.add_discount("d1", "milk 20 tomato 50", "milk quantity = 20")
        self.discount_policy.add_discount("d2", "milk 30 tomato 50", "milk quantity = 20")
        self.discount_policy.add_discount("d3", "milk 40 tomato 50", "milk quantity = 30")
        self.discount_policy.add_discount("d4", "milk 20 tomato 50", "milk quantity = 20", True)
        length = len(self.discount_policy.discount_dict)
        self.assertTrue(length == 4)








