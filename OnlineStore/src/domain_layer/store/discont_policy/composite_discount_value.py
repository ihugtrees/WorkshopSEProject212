from OnlineStore.src.domain_layer.store.discont_policy.discount_value import DiscountValue


class CompositeDiscountValue(DiscountValue):

    def __init__(self, left_discount: DiscountValue, right_discount: DiscountValue, operator: str):
        self.left_discount = left_discount
        self.right_discount = right_discount
        self.operator = operator

    def calc_discount(self, basketDTO):
        left_value = self.left_discount.calc_discount(basketDTO)
        right_value = self.right_discount.calc_discount(basketDTO)
        ans = [0, 0]
        ans[1] = left_value[1]
        if self.operator == "MAX":
            ans[0] = min(left_value[0], right_value[0])
        elif self.operator == "AND":
            d1 = left_value[1]-left_value[0]
            d2 = right_value[1]-right_value[0]
            ans[0] = ans[1]-(d1+d2)
        else:
            raise Exception ("operator should be MAX or AND")
        return ans


