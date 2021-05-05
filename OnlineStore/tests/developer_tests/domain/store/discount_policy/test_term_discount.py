from unittest import TestCase

from OnlineStore.src.domain.store.discont_policy.atomic_term import AtomicTerm
from OnlineStore.src.domain.store.discont_policy.term_discount import TermDiscount
from OnlineStore.src.domain.store.store import Store


class TestTermDiscount(TestCase):
    def setUp(self):
        self.basketDTO = basketDTO = {
            "milk": (20, 20),  # key - product name value - (quantity, price)
            "yogurt": (50, 10)
        }



    def test_calc_term_atomic(self):
        t1: TermDiscount = TermDiscount("milk quantity = 20")
        self.assertTrue(t1.term.calc_term(self.basketDTO))
        t2: TermDiscount = TermDiscount("milk quantity = 21")
        self.assertFalse(t2.term.calc_term(self.basketDTO))
        t3: TermDiscount = TermDiscount("milk quantity > 15")
        self.assertTrue(t3.term.calc_term(self.basketDTO))
        t4: TermDiscount = TermDiscount("milk quantity < 15")
        self.assertFalse(t4.term.calc_term(self.basketDTO))
        t5: TermDiscount = TermDiscount("milk price = 400")
        self.assertTrue(t5.term.calc_term(self.basketDTO))
        t6: TermDiscount = TermDiscount("milk price = 401")
        self.assertFalse(t6.term.calc_term(self.basketDTO))
        t7: TermDiscount = TermDiscount("milk price > 350")
        self.assertTrue(t7.term.calc_term(self.basketDTO))
        t8: TermDiscount = TermDiscount("milk price < 500")
        self.assertTrue(t8.term.calc_term(self.basketDTO))

    def test_calc_term_composite(self):
        t1: TermDiscount = TermDiscount("milk quantity = 20 AND milk price = 400")
        self.assertTrue(t1.term.calc_term(self.basketDTO))
        t1: TermDiscount = TermDiscount("milk quantity = 20 AND milk price = 500")
        self.assertFalse(t1.term.calc_term(self.basketDTO))
        t1: TermDiscount = TermDiscount("milk quantity = 20 OR milk price = 17")
        self.assertTrue(t1.term.calc_term(self.basketDTO))
        t1: TermDiscount = TermDiscount("milk quantity = 22 OR milk price = 450")
        self.assertFalse(t1.term.calc_term(self.basketDTO))

    def test_calc_term_composite_times(self):
        t1: TermDiscount = TermDiscount("milk quantity = 20 OR milk price = 400 AND yogurt quantity = 25")
        self.assertTrue(t1.term.calc_term(self.basketDTO))
        t1: TermDiscount = TermDiscount("milk quantity = 20 AND milk price = 45 OR yogurt quantity = 50")
        self.assertTrue(t1.term.calc_term(self.basketDTO))



