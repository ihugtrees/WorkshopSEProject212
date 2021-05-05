from OnlineStore.src.domain.store.discont_policy.term import Term


class CompositeTerm(Term):

    def __init__(self, operator: str, left_term: Term, right_term: Term):
        self.operator = operator
        self.left_term = left_term
        self.right_term = right_term


    def calc_term(self, basketDTO):
        if self.operator == "OR":
            return self.left_term.calc_term(basketDTO) or self.right_term.calc_term(basketDTO)
        if self.operator == "AND":
            return self.left_term.calc_term(basketDTO) and self.right_term.calc_term(basketDTO)
        # if self.operator == "XOR":
        #     return self.left_term.calc_term()  self.right_term.calc_term()




