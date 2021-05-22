from OnlineStore.src.domain.store.buying_policy.buying_term import BuyingTerm
from OnlineStore.src.domain.store.discont_policy.term import Term


class AtomicBuyingTerm(BuyingTerm):

    def __init__(self, product_name: str, quantity_or_price: str, operator: str, value: int , category: str = False,
                   no_flag=False):
        self.product_name = product_name
        self.quantity_or_price = quantity_or_price
        self.operator = operator
        self.value = value
        self.category = category
        #self.user_name_flag = user_name_flag
        #self.age_flag = age_flag
        self.no_flag = no_flag
       # self.age_value = age_value
        #self. basketDTO = basketDTO  # key - product name value - (quantity, price, category)
        #userDTO => touple of (age, username)

    def calc_term(self, basketDTO, userDTO):
        if self.no_flag:
            return not self.calc_termP(basketDTO, userDTO)
        return self.calc_termP(basketDTO, userDTO)

    def calc_termP(self, basketDTO, userDTO):
        #if self.age_flag:
         #   self.calc(userDTO[0])
        if self.product_name not in basketDTO:
            basketDTO[self.product_name] = (0, 0, "none")
        if not self.category:
            return self.calc_regular_term(basketDTO)
        return self.calc_category_term(basketDTO)

    def calc_regular_term(self, basketDTO) -> bool:
        real_value = 0
        if self.quantity_or_price == "q":
            real_value = basketDTO[self.product_name][0]
        else:
            real_value = basketDTO[self.product_name][0] * basketDTO[self.product_name][1]
        return self.calc(real_value)

    def calc_category_term(self, basketDTO):
        sum_quantity = 0
        sum_price = 0
        if self.product_name == "ALL":
            for p in basketDTO:
                sum_quantity += basketDTO[p][0]
                sum_price += basketDTO[p][0] * basketDTO[p][1]
        else:
            for p in basketDTO:
                if basketDTO[p][2] == self.product_name:
                    sum_quantity += basketDTO[p][0]
                    sum_price += basketDTO[p][0] * basketDTO[p][1]

        real_value = 0
        if self.quantity_or_price == "q":
            real_value = sum_quantity
        else:
            real_value = sum_price
        return self.calc(real_value)

    def calc(self, real_value):
        if self.operator == ">":
            return real_value > self.value
        if self.operator == "<":
            return real_value < self.value
        if self.operator == "=":
            return int(real_value) == int(self.value)

    #def calc_age_flag(self):
     #   if




