from OnlineStore.src.domain.store.discont_policy.term import Term


class AtomicTerm(Term):

    def __init__(self, product_name: str, quantity_or_price: str, operator: str, value: int , category: str = None):
        self.product_name = product_name
        self.quantity_or_price = quantity_or_price
        self.operator = operator
        self.value = value
        self.category = category
        #self. basketDTO = basketDTO  # key - product name value - (quantity, price)

    def calc_term(self, basketDTO):
        if self.category == None:
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
        sum_price = 0;
        for p in basketDTO:
            sum_quantity += basketDTO[p][0]
            sum_price += basketDTO[p][0] * basketDTO[p][1]
        real_value = 0
        if self.quantity_or_price == "q":
            real_value = sum_quantity
        else:
            real_value = sum_price
        self.calc(real_value)

    def calc(self, real_value):
        if self.operator == ">":
            return real_value > self.value
        if self.operator == "<":
            return real_value < self.value
        if self.operator == "=":
            return real_value == self.value






