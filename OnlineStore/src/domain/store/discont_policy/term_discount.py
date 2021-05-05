from OnlineStore.src.domain.store.discont_policy.atomic_term import AtomicTerm
from OnlineStore.src.domain.store.discont_policy.composite_term import CompositeTerm
from OnlineStore.src.domain.store.discont_policy.term import Term


class TermDiscount:

    def __init__(self, term_string: str):
        term: Term = self.make_term_from_string(term_string)
        self.term = term

    def make_term_from_string(self, s_term: str):
        i = 0
        for i in range(len(s_term)):
            if s_term[i] == "O" and s_term[i+1] == "R":
                left_term = self.make_term_from_string(s_term[0:i])
                right_term = self.make_term_from_string(s_term[i+3: len(s_term)])
                return CompositeTerm("OR", left_term, right_term)
            elif s_term[i] == "A" and s_term[i+1] == "N" and s_term[i+2] == "D":
                left_term = self.make_term_from_string(s_term[0:i])
                right_term = self.make_term_from_string(s_term[i + 4: len(s_term)])
                return CompositeTerm("AND", left_term, right_term)
            i = i + 1
        return self.make_atomic_term_from_string(s_term)

    def make_atomic_term_from_string(self, s_term):
        q_or_p = None
        if "quantity" in s_term:
            q_or_p = "q"
        else:
            q_or_p = "p"
        length = len(s_term)
        i: int = 0
        word = 0
        product_name = ""
        start_operator: int = 0
        operator = ""
        value = 0
        for i in range(length):
            if word == 0 and s_term[i] == " ":
                product_name = s_term[0:i]
                word = word + 1
            elif word == 1 and s_term[i] == " ":
                start_operator = i+1
                word = word + 1
            elif word == 2 and s_term[i] == " ":
                operator = s_term[start_operator: i]
                word = word + 1
                value = int(s_term[i+1: length])
            i = i + 1
        return AtomicTerm(product_name, q_or_p, operator, value)











