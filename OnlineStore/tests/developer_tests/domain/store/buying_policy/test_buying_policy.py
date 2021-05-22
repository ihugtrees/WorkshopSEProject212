from unittest import TestCase

from OnlineStore.src.domain_layer.store.buying_policy.buying_policy import BuyingPolicy
from OnlineStore.src.domain_layer.store.discont_policy.atomic_term import AtomicTerm
from OnlineStore.src.domain_layer.store.discont_policy.discount_policy import DiscountPolicy
from OnlineStore.src.domain_layer.store.discont_policy.term_discount import TermDiscount
from OnlineStore.src.domain_layer.store.store import Store


class TestBuyingPolicy(TestCase):
    def setUp(self):
        self.basketDTO = basketDTO = {
            "milk": (20, 20, "milk"),  # key - product name value - (quantity, price,category)
            "yogurt": (50, 10, "milk"),
            "avocado": (30, 4, "veg")
        }
        self.buying_policy = BuyingPolicy()


    def test_add_discount(self):
        self.buying_policy.add_buying_term("d1", "milk quantity > 20")
        self.buying_policy.add_buying_term("d2", "milk quantity < 20")
        self.buying_policy.add_buying_term("d3",  "milk quantity = 30")
        self.buying_policy.add_buying_term("d4",  "milk quantity = 20")
        length = len(self.buying_policy.terms_dict)
        self.assertTrue(length == 4)










