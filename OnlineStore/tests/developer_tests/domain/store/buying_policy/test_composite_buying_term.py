from unittest import TestCase

from OnlineStore.src.domain.store.buying_policy.atomic_buying_term import AtomicBuyingTerm
from OnlineStore.src.domain.store.buying_policy.atomic_buying_user_term import AtomicBuyingUserTerm
from OnlineStore.src.domain.store.buying_policy.composite_buying_term import CompositeBuyingTerm
from OnlineStore.src.domain.store.discont_policy.atomic_term import AtomicTerm
from OnlineStore.src.domain.store.discont_policy.composite_term import CompositeTerm
from OnlineStore.src.domain.store.store import Store


class TestCompositeBuyingTerm(TestCase):
    def setUp(self):
        product_name = "milki"
        quantity_or_price = "q"
        operator = "="
        value = 20
        self.basketDTO = basketDTO = {
            "milki": (20, 50, "milki"),  # key - product name value - (quantity, price)
            "shoko": (20, 50, "milki"),
            "avocado": (20, 50, "veg")
        }
        self.userDTO = {
            "age": 20,
            "user_name": "moshe"
        }
        self.atomic_term4: AtomicBuyingTerm = AtomicBuyingTerm(product_name, quantity_or_price, operator, value) # True
        self.atomic_term1: AtomicBuyingUserTerm = AtomicBuyingUserTerm("age", ">", 18)  # True
        self.atomic_term2: AtomicBuyingUserTerm = AtomicBuyingUserTerm("age", ">", 22)  # False
        self.atomic_term3: AtomicBuyingUserTerm = AtomicBuyingUserTerm("age", "<", 22, no_flag=True)  # False
        #self.comp1: CompositeBuyingTerm = CompositeBuyingTerm("AND", self.atomic_term4, self.atomic_term1)  # True
        #self.comp2: CompositeBuyingTerm = CompositeBuyingTerm("AND", self.atomic_term2, self.atomic_term1)  # false

    def test_calc_term(self):
        comp1: CompositeBuyingTerm = CompositeBuyingTerm("AND", self.atomic_term4, self.atomic_term1)  # True
        self.assertTrue(comp1.calc_term(self.basketDTO, self.userDTO))
        comp2: CompositeBuyingTerm = CompositeBuyingTerm("AND", self.atomic_term2, self.atomic_term1)  # false
        self.assertFalse(comp2.calc_term(self.basketDTO, self.userDTO))
        self.assertFalse(self.atomic_term3.calc_term(self.basketDTO, self.userDTO))
        comp3 = CompositeBuyingTerm("OR", self.atomic_term3, comp1 )
        self.assertTrue(comp3.calc_term(self.basketDTO, self.userDTO))







