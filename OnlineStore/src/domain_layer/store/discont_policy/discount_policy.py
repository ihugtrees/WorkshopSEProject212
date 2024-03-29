from OnlineStore.src.data_layer import user_entity, store_data
from OnlineStore.src.domain_layer.store.discont_policy.composite_discount_value import CompositeDiscountValue
from OnlineStore.src.domain_layer.store.discont_policy.composite_term import CompositeTerm
from OnlineStore.src.domain_layer.store.discont_policy.term_discount import TermDiscount
from OnlineStore.src.dto.user_dto import UserDTO


class DiscountPolicy:

    def __init__(self):
        self.discount_dict = dict()  # key - discount name, value- (TermDiscount, description)

    def add_discount(self, discount_name: str, discount_value: str, discount_term: str = None,
                     discount_value_type: bool = False, store=None):
        if discount_name in self.discount_dict:
            raise Exception("discount name already exist")
        if discount_term is None or discount_term == "None":
            self.discount_dict[discount_name] = (TermDiscount(term_string=discount_term,
                                                              discount_description_products=discount_value,
                                                              discount_description_categories=discount_value_type),
                                                 "term: " + "None" + ", value: " + discount_value)
            store_data.add_discount_policy(store, discount_name, "None", discount_value, category_flag=discount_value_type)
        else:
            self.discount_dict[discount_name] = (TermDiscount(term_string=discount_term,
            discount_description_products=discount_value, discount_description_categories = discount_value_type),
                                             "term: " + discount_term+ ", value: " + discount_value)
            store_data.add_discount_policy(store, discount_name, discount_term, discount_value, category_flag=discount_value_type)

    def combine_discount(self, d1_name, d2_name, operator: str, new_name):
        if new_name in self.discount_dict:
            raise Exception("discount name already exist")
        if d1_name not in self.discount_dict or d2_name not in self.discount_dict:
            raise Exception("wrong discount name")
        t1 = self.discount_dict[d1_name]
        t2 = self.discount_dict[d2_name]
        self.discount_dict[new_name] = (self.combine_discount_private(t1[0], t2[0], operator),
                                        self.discount_dict[d1_name][1]+" "+ operator+ " "+ self.discount_dict[d2_name][1])
        self.discount_dict.pop(d1_name)
        self.discount_dict.pop(d2_name)

    def combine_discount_private(self, term_d1: TermDiscount, term_d2: TermDiscount, operator):
        term1 = term_d1.term
        term2 = term_d2.term
        value1 = term_d1.products_discount
        value2 = term_d2.products_discount
        composite_term = CompositeTerm("OR", term1, term2)
        composite_val = CompositeDiscountValue(value1, value2, operator)
        ans = TermDiscount()
        ans.term = composite_term
        ans.products_discount = composite_val
        return ans

    def calc_price(self, basketDTO):
        min_price = -1
        for d in self.discount_dict:
            price_after_discount = self.discount_dict[d][0].calc_price(basketDTO)
            if min_price == -1 or price_after_discount < min_price:
                min_price = price_after_discount
        return min_price

    def show_discount_policy(self):
        ans = ""
        for t in self.discount_dict:
            ans += self.discount_dict[t][1] + "   "
        return ans

    def delete_discount(self, term_name: str):
        if term_name not in self.discount_dict:
            raise Exception(term_name + "not exist")
        self.discount_dict.pop(term_name)
