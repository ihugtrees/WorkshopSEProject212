from OnlineStore.src.domain.store.buying_policy.buying_term import BuyingTerm
from OnlineStore.src.domain.store.discont_policy.term import Term


class AtomicBuyingUserTerm(BuyingTerm):

    def __init__(self, type_flag: str, operator: str, value: int, no_flag=False):
        self.type_flag = type_flag
        self.operator = operator
        self.value = value
        self.no_flag = no_flag
        # userDTO => dict (type, val)

    def calc_term(self, basketDTO, userDTO):
        if self.no_flag:
            return not self.calc_termP(userDTO)
        return self.calc_termP(userDTO)

    def calc_termP(self, userDTO):
        real_value = userDTO[self.type_flag]
        return self.calc(real_value)

    def calc(self, real_value):
        if self.operator == ">":
            return real_value > self.value
        if self.operator == "<":
            return real_value < self.value
        if self.operator == "=":
            return int(real_value) == int(self.value)
