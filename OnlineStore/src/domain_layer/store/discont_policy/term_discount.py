from OnlineStore.src.domain_layer.store.discont_policy.atomic_term import AtomicTerm
from OnlineStore.src.domain_layer.store.discont_policy.composite_discount_value import CompositeDiscountValue
from OnlineStore.src.domain_layer.store.discont_policy.composite_term import CompositeTerm
from OnlineStore.src.domain_layer.store.discont_policy.atomic_discount_value import DiscountValue, AtomicDiscountValue
from OnlineStore.src.domain_layer.store.discont_policy.term import Term


class TermDiscount:

    def __init__(self, term_string: str = None, discount_description_products: str = None,
                 discount_description_categories=False):
        term: Term = self.make_term_from_string(term_string)
        self.term = term
        if discount_description_products is not None:
            self.products_discount: AtomicDiscountValue = self.make_products_disc_from_str(
                discount_description_products, discount_description_categories)

    def make_term_from_string(self, s_term: str):
        if s_term is None:
            return None
        i = 0
        for i in range(len(s_term)):
            if s_term[i] == "O" and s_term[i + 1] == "R":
                left_term = self.make_term_from_string(s_term[0:i])
                right_term = self.make_term_from_string(s_term[i + 3: len(s_term)])
                return CompositeTerm("OR", left_term, right_term)
            elif s_term[i] == "A" and s_term[i + 1] == "N" and s_term[i + 2] == "D":
                left_term = self.make_term_from_string(s_term[0:i])
                right_term = self.make_term_from_string(s_term[i + 4: len(s_term)])
                return CompositeTerm("AND", left_term, right_term)
            elif s_term[i] == "X" and s_term[i + 1] == "O" and s_term[i + 2] == "R":
                left_term = self.make_term_from_string(s_term[0:i])
                right_term = self.make_term_from_string(s_term[i + 4: len(s_term)])
                return CompositeTerm("XOR", left_term, right_term)

            i = i + 1
        return self.make_atomic_term_from_string(s_term)

    def make_atomic_term_from_string(self, s_term):
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
        return AtomicTerm(product_name, q_or_p, operator, value, category=categort_flag)

    def make_products_disc_from_str(self, str_d: str, category_flag):
        dictP = dict()
        start_word = 0
        first_Word = ""
        is_fist = True
        for i in range(len(str_d)):
            if str_d[i] == " " and is_fist:
                first_Word = str_d[start_word: i]
                is_fist = False
                start_word = i + 1
            elif str_d[i] == " " and (not is_fist):
                dictP[first_Word] = str_d[start_word: i]
                is_fist = True
                start_word = i + 1
            i = i + 1
        dictP[first_Word] = str_d[start_word: len(str_d)]
        return AtomicDiscountValue(dictP, category_flag)

    def calc_term(self, basketDTO):
        if self.term is None:
            return Term # supose to be return true
        else:
            return self.term.calc_term(basketDTO)

    def calc_price(self, basketDTO):
        new_price, original_price = self.products_discount.calc_discount(basketDTO)
        if self.calc_term(basketDTO):
            return new_price
        else:
            return original_price
