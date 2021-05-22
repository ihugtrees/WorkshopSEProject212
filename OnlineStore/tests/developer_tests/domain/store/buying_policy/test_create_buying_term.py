from unittest import TestCase

from OnlineStore.src.domain_layer.store.buying_policy.create_buying_term import CreateBuyingTerm
from OnlineStore.src.domain_layer.store.discont_policy.atomic_term import AtomicTerm
from OnlineStore.src.domain_layer.store.discont_policy.term_discount import TermDiscount
from OnlineStore.src.domain_layer.store.store import Store


class TestCreateBuyingTerm(TestCase):
    def setUp(self):
        self.basketDTO = basketDTO = {
            "milk": (20, 20, "milk"),  # key - product name value - (quantity, price)
            "yogurt": (50, 10, "milk"),
            "avocado": (32, 4, "veg")
        }
        self.userDTO = {
            "age": 20
        }


    def test_create_atomic(self):
        c1: CreateBuyingTerm = CreateBuyingTerm("milk quantity = 20")
        self.assertTrue(c1.term.product_name == "milk" and c1.term.quantity_or_price == "q" and
                        c1.term.operator == "=" and c1.term.value == 20)

    def test_create_atomic_user(self):
        c2: CreateBuyingTerm = CreateBuyingTerm("-U age > 18")
        self.assertTrue(c2.term.type_flag == "age" and c2.term.operator == ">" and c2.term.value == 18)

    def test_Create_composite_term(self):
        c1: CreateBuyingTerm = CreateBuyingTerm("milk quantity = 20 OR milk price = 400 AND yogurt quantity = 25")
        self.assertTrue(c1.term.calc_term(self.basketDTO, self.userDTO))
        c2: CreateBuyingTerm = CreateBuyingTerm("-U age = 20 AND milk price = 45 OR yogurt quantity = 50")
        self.assertTrue(c2.term.calc_term(self.basketDTO, self.userDTO))
        c3: CreateBuyingTerm = CreateBuyingTerm("-U age = 18 AND milk price = 45 OR yogurt quantity = 50")
        self.assertFalse(c3.term.calc_term(self.basketDTO, self.userDTO))
        c4: CreateBuyingTerm = CreateBuyingTerm("-U age = 20 AND milk price = 45 OR yogurt quantity = 50")
        self.assertTrue(c4.term.calc_term(self.basketDTO, self.userDTO))
        c5: CreateBuyingTerm = CreateBuyingTerm("-U age = 20 ONLY_IF milk price = 45 OR yogurt quantity = 50")
        self.assertTrue(c5.term.calc_term(self.basketDTO, self.userDTO))
        c6: CreateBuyingTerm = CreateBuyingTerm("-U age = 21 ONLY_IF milk price = 45 AND yogurt quantity = 50")
        self.assertTrue(c6.term.calc_term(self.basketDTO, self.userDTO))
        c7: CreateBuyingTerm = CreateBuyingTerm("-U age = 20 ONLY_IF milk price = 45 AND yogurt quantity = 50")
        self.assertFalse(c7.term.calc_term(self.basketDTO, self.userDTO))

    def test_calc_term_atomic_category(self):
        c1: CreateBuyingTerm = CreateBuyingTerm("-C milk quantity = 20")
        self.assertFalse(c1.calc_term(self.basketDTO, self.userDTO))
        c2: CreateBuyingTerm = CreateBuyingTerm("-C milk quantity = 70")
        self.assertTrue(c2.calc_term(self.basketDTO, self.userDTO))
        c3: CreateBuyingTerm = CreateBuyingTerm("-C ALL quantity = 102")
        self.assertTrue(c3.calc_term(self.basketDTO, self.userDTO))





