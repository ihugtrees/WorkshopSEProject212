from unittest import TestCase

from OnlineStore.src.domain_layer.store.discont_policy.atomic_discount_value import AtomicDiscountValue
from OnlineStore.src.domain_layer.store.discont_policy.atomic_term import AtomicTerm
from OnlineStore.src.domain_layer.store.store import Store


class TestAtomicDiscountValue(TestCase):
    def setUp(self):

        dictP = {"milki": 20, "shoko": 30, "tomato": 40}
        self.basketDTO = basketDTO = {
            "milki": (20, 50, "milki") , # key - product name value - (quantity, price)
            "shoko": (20, 50, "milki"),
            "avocado": (20, 50, "veg")
        }
        self.atomic_value1: AtomicDiscountValue = AtomicDiscountValue(dictP, False)
        dictP2= {"milki": 40, "shoko": 30, "tomato": 40}
        self.atomic_value2: AtomicDiscountValue = AtomicDiscountValue(dictP2, True)


    def test_calc_price(self):
        new_price, origin_price = self.atomic_value1.calc_discount(self.basketDTO)
        self.assertTrue(new_price == 2500)
        self.assertTrue(origin_price == 3000)
        new_price2, origin_price2 = self.atomic_value2.calc_discount(self.basketDTO)
        self.assertTrue(new_price2 == 2200)
        self.assertTrue(origin_price2 == 3000)







