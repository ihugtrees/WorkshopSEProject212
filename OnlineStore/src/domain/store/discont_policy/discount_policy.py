from OnlineStore.src.domain.store.discont_policy.term_discount import TermDiscount
from OnlineStore.src.dto.user_dto import UserDTO

class DiscountPolicy:

    def __init__(self):
        self.discount_dict = dict()  # key - discount name, value- TermDiscount


    def add_discount(self, discount_name: str, discount_value: str, discount_term: str=None):
        if discount_name in self.discount_dict:
            raise Exception("discount name already exist")
        self.discount_dict[discount_value] = TermDiscount(discount_term=discount_term, discount_description_products=discount_value)
        #here   ggggggggggggggggg


    # def elligible_for_discount(user: UserDTO):
    #     pass