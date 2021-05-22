from OnlineStore.src.domain.store.discont_policy.discount_value import DiscountValue


class AtomicDiscountValue(DiscountValue):

    def __init__(self, dictP, category_flag=False):
        self.dictP = dictP
        self.category_flag = category_flag

    def calc_discount(self, basketDTO):
        original_price = 0
        new_price = 0
        if not self.category_flag:
            for p in basketDTO:
                origin = basketDTO[p][0] * basketDTO[p][1]
                original_price += origin
                if p in self.dictP:
                    new_price += (origin * (100-int(self.dictP[p]))) / 100
                else:
                    new_price += origin
        else:
            for p in basketDTO:
                origin = basketDTO[p][0] * basketDTO[p][1]
                original_price += origin
                if basketDTO[p][2] in self.dictP:
                    new_price += (origin * (100-int(self.dictP[basketDTO[p][2]]))) / 100
                else:
                    new_price += origin
        return new_price, original_price
