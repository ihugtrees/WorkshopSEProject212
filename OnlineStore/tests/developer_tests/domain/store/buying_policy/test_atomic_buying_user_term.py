from unittest import TestCase

from OnlineStore.src.domain.store.buying_policy.atomic_buying_term import AtomicBuyingTerm
from OnlineStore.src.domain.store.buying_policy.atomic_buying_user_term import AtomicBuyingUserTerm
from OnlineStore.src.domain.store.discont_policy.atomic_term import AtomicTerm
from OnlineStore.src.domain.store.store import Store


class TestAtomicBuyingUserTerm(TestCase):
    def setUp(self):

        # product_name = "milki"
        # quantity_or_price = "q"
        # operator = "="
        # value = 100
        self.basketDTO = basketDTO = {
            "milki": (20, 50, "milki") , # key - product name value - (quantity, price , category)
            "shoko": (20, 50, "milki"),
            "avocado": (20, 50, "veg")
        }
        self.userDTO = {
            "age": 20,
            "user_name": "moshe"
        }
        self.atomic_term1: AtomicBuyingUserTerm = AtomicBuyingUserTerm("age", ">", 18)
        self.atomic_term2: AtomicBuyingUserTerm = AtomicBuyingUserTerm("age", ">", 22)
        self.atomic_term3: AtomicBuyingUserTerm = AtomicBuyingUserTerm("age", "<", 22, no_flag=True)






    def test_calc_term(self):
        self.assertTrue(self.atomic_term1.calc_term(self.basketDTO, self.userDTO))
        self.assertFalse(self.atomic_term2.calc_term(self.basketDTO, self.userDTO))
        self.assertFalse(self.atomic_term3.calc_term(self.basketDTO, self.userDTO))
        #self.assertTrue(self.atomic_term1.calc_term(self.basketDTO, self.userDTO))




