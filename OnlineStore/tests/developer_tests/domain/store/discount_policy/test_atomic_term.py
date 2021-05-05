from unittest import TestCase

from OnlineStore.src.domain.store.discont_policy.atomic_term import AtomicTerm
from OnlineStore.src.domain.store.store import Store


class TestAtomicTerm(TestCase):
    def setUp(self):

        product_name = "milk"
        quantity_or_price = "q"
        operator = "="
        value = 100
        self.basketDTO = basketDTO = {
            "milk": (20, 50)  # key - product name value - (quantity, price)
        }
        self.atomic_term1: AtomicTerm = AtomicTerm(product_name, quantity_or_price, operator, value)



    def test_calc_term(self):
        self.assertFalse(self.atomic_term1.calc_term(self.basketDTO))
        self.atomic_term1.value = 20
        self.assertTrue(self.atomic_term1.calc_term(self.basketDTO))


