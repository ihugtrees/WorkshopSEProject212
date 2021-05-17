from OnlineStore.src.domain.store.buying_policy.buying_term import BuyingTerm
from OnlineStore.src.domain.store.discont_policy.term import Term


class CompositeBuyingTerm(BuyingTerm):

    def __init__(self, operator: str, left_term: BuyingTerm, right_term: BuyingTerm, no_flag=False):
        self.operator = operator
        self.left_term = left_term
        self.right_term = right_term
        self.no_flag = no_flag

    def calc_term(self, basketDTO, userDTO):
        if self.no_flag:
            return not self.calc_termP(basketDTO, userDTO)
        return self.calc_termP(basketDTO, userDTO)

    def calc_termP(self, basketDTO, userDTO):
        if self.operator == "OR":
            return self.left_term.calc_term(basketDTO, userDTO) or self.right_term.calc_term(basketDTO, userDTO)
        if self.operator == "AND":
            return self.left_term.calc_term(basketDTO, userDTO) and self.right_term.calc_term(basketDTO, userDTO)
        if self.operator == "ONLY_IF":
            return (not self.left_term.calc_term(basketDTO, userDTO)) or self.right_term.calc_term(basketDTO, userDTO)




