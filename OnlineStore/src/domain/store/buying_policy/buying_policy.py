from typing import Dict

from OnlineStore.src.domain.store.buying_policy.buying_term import BuyingTerm
from OnlineStore.src.domain.store.buying_policy.create_buying_term import CreateBuyingTerm
from OnlineStore.src.dto.user_dto import UserDTO


class BuyingPolicy:
    def __init__(self):
        self.terms_dict: Dict[str, BuyingTerm] = dict()  # key - term name, val - BuyingTerm

    def elligible_for_buying(self, user: UserDTO, basket) -> None:
        ans = True
        for t in self.terms_dict:
            ans = ans and self.terms_dict[t].calc_term(basket, user)
        if not ans:
            raise Exception("buying policy fail")

    def add_buying_term(self, term_name: str, s_term: str, no_flag=False):
        temp: CreateBuyingTerm = CreateBuyingTerm(s_term, no_flag)
        self.terms_dict[term_name] = temp.term
