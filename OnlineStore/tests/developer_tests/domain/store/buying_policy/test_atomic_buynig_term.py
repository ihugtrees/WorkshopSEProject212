from unittest import TestCase

from OnlineStore.src.domain.store.buying_policy.atomic_buying_term import AtomicBuyingTerm
from OnlineStore.src.domain.store.discont_policy.atomic_term import AtomicTerm
from OnlineStore.src.domain.store.store import Store


class TestAtomicBuyingTerm(TestCase):
    def setUp(self):

        product_name = "milki"
        quantity_or_price = "q"
        operator = "="
        value = 100
        self.basketDTO = basketDTO = {
            "milki": (20, 50, "milki") , # key - product name value - (quantity, price)
            "shoko": (20, 50, "milki"),
            "avocado": (20, 50, "veg")
        }
        self.userDTO = {
            "age": 20,
            "user_name": "moshe"
        }
        self.atomic_term1: AtomicBuyingTerm = AtomicBuyingTerm(product_name, quantity_or_price, operator, value)



    def test_calc_term(self):
        self.assertFalse(self.atomic_term1.calc_term(self.basketDTO, self.userDTO))
        self.atomic_term1.value = 20
        self.assertTrue(self.atomic_term1.calc_term(self.basketDTO, self.userDTO))
        self.atomic_term1.category = True
        self.assertFalse(self.atomic_term1.calc_term(self.basketDTO, self.userDTO))
        self.atomic_term1.value = 40
        self.assertTrue(self.atomic_term1.calc_term(self.basketDTO, self.userDTO))




