from OnlineStore.src.domain.store.buying_policy.atomic_buying_term import AtomicBuyingTerm
from OnlineStore.src.domain.store.buying_policy.atomic_buying_user_term import AtomicBuyingUserTerm
from OnlineStore.src.domain.store.buying_policy.buying_term import BuyingTerm
from OnlineStore.src.domain.store.buying_policy.composite_buying_term import CompositeBuyingTerm


class CreateBuyingTerm:

    def __init__(self, term_string: str, no_flag=False):
        term: BuyingTerm = self.make_term_from_string(term_string, no_flag)
        self.term = term
        # self.no_flag = no_flag

    def make_term_from_string(self, s_term: str, no_flag=False):
        if s_term is None:
            return None
        i = 0
        for i in range(len(s_term)):
            if s_term[i] == "O" and s_term[i + 1] == "R":
                left_term = self.make_term_from_string(s_term[0:i])
                right_term = self.make_term_from_string(s_term[i + 3: len(s_term)])
                return CompositeBuyingTerm("OR", left_term, right_term, no_flag=no_flag)
            elif s_term[i] == "A" and s_term[i + 1] == "N" and s_term[i + 2] == "D":
                left_term = self.make_term_from_string(s_term[0:i])
                right_term = self.make_term_from_string(s_term[i + 4: len(s_term)])
                return CompositeBuyingTerm("AND", left_term, right_term, no_flag=no_flag)
            elif s_term[i] == "O" and s_term[i + 1] == "N" and s_term[i + 2] == "L":
                left_term = self.make_term_from_string(s_term[0:i])
                right_term = self.make_term_from_string(s_term[i + 8: len(s_term)])
                return CompositeBuyingTerm("ONLY_IF", left_term, right_term, no_flag=no_flag)
            i = i + 1
        return self.make_atomic_term_from_string(s_term, no_flag=no_flag)

    def make_atomic_term_from_string(self, s_term, no_flag=False):
        if "-U" in s_term:
            return self.make_user_term(s_term[3: len(s_term)], no_flag=no_flag)
        q_or_p = None
        if "quantity" in s_term:
            q_or_p = "q"
        else:
            q_or_p = "p"
        categort_flag = False
        if "-C" in s_term:
            categort_flag = True
            s_term = s_term[3: len(s_term)]
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
                start_operator = i + 1
                word = word + 1
            elif word == 2 and s_term[i] == " ":
                operator = s_term[start_operator: i]
                word = word + 1
                value = int(s_term[i + 1: length])
            i = i + 1
        return AtomicBuyingTerm(product_name, q_or_p, operator, value, category=categort_flag, no_flag=no_flag)

    def make_user_term(self, s_term, no_flag=False):
        length = len(s_term)
        i: int = 0
        word = 0
        type_flag = ""
        start_operator: int = 0
        operator = ""
        value = 0
        for i in range(length):
            if word == 0 and s_term[i] == " ":
                type_flag = s_term[0:i]
                word = word + 1
                start_operator = i + 1
            elif word == 1 and s_term[i] == " ":
                operator = s_term[start_operator: i]
                word = word + 1
                value = int(s_term[i + 1: length])
            i = i + 1
        return AtomicBuyingUserTerm(type_flag, operator, value, no_flag)

    def calc_term(self, basketDTO, userDTO):
        return self.term.calc_term(basketDTO, userDTO)

    def calc_price(self, basketDTO):
        new_price, original_price = self.products_discount.calc_discount(basketDTO)
        if self.calc_term(basketDTO):
            return new_price
        else:
            return original_price
