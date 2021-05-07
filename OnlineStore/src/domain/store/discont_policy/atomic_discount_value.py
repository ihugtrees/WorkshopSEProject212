from OnlineStore.src.domain.store.discont_policy.discount_value import DiscountValue


class AtomicDiscountValue(DiscountValue):

    def __init__(self, dictP):
        self.dictP = dictP

    def calc_discount(self, basketDTO):
        original_price = 0
        new_price = 0
        for p in basketDTO:
            origin = basketDTO[p][0] * basketDTO[p][1]
            original_price += origin
            if p in self.dictP:
                new_price += (origin * basketDTO[p]) / 100
            else:
                new_price += origin
        return new_price, original_price
