from unittest import TestCase

from OnlineStore.src.domain_layer.store.discont_policy.atomic_term import AtomicTerm
from OnlineStore.src.domain_layer.store.discont_policy.composite_term import CompositeTerm
from OnlineStore.src.domain_layer.store.store import Store


class TestCompositeTerm(TestCase):
    def setUp(self):

        product_name = "milki"
        quantity_or_price = "q"
        operator = "="
        value = 100
        self.basketDTO = basketDTO = {
            "milki": (100, 50, "milki") , # key - product name value - (quantity, price)
            "shoko": (20, 50, "milki"),
            "avocado": (20, 50, "veg")
        }
        atomic_term1: AtomicTerm = AtomicTerm(product_name, quantity_or_price, operator, value)
        product_name = "milki"
        quantity_or_price = "q"
        operator = "="
        value = 50
        atomic_term2: AtomicTerm = AtomicTerm(product_name, quantity_or_price, operator, value)
        self.composite = CompositeTerm("AND", atomic_term1, atomic_term2)
        self.composite2 = CompositeTerm("OR", atomic_term1, atomic_term2)

    def test_calc_term(self):
        self.assertTrue(self.composite2.calc_term(self.basketDTO))
        self.assertFalse(self.composite.calc_term(self.basketDTO))






