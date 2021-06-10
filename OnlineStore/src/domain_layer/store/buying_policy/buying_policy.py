from typing import Dict

from OnlineStore.src.data_layer import user_entity, store_data
from OnlineStore.src.domain_layer.store.buying_policy.buying_term import BuyingTerm
from OnlineStore.src.domain_layer.store.buying_policy.create_buying_term import CreateBuyingTerm
from OnlineStore.src.dto.user_dto import UserDTO


class BuyingPolicy:
    def __init__(self):
        self.terms_dict: Dict[str, (BuyingTerm, str)] = dict()  # key - term name, val - (BuyingTerm, description)

    def eligible_for_buying(self, user: UserDTO, basket) -> None:
        ans = True
        for t in self.terms_dict:
            ans = ans and self.terms_dict[t][0].calc_term(basket, user)
        if not ans:
            raise Exception("buying policy fail")

    def add_buying_term(self, term_name: str, s_term: str, no_flag=False, store=None):
        temp: CreateBuyingTerm = CreateBuyingTerm(s_term, no_flag)
        if term_name in self.terms_dict:
            raise Exception("name already exist, please choose another name")
        self.terms_dict[term_name] = (temp.term, s_term)
        store_data.add_buying_policy(store, term_name, s_term)

    def delete_buying_term(self, term_name: str):
        if term_name in self.terms_dict:
            return self.terms_dict.pop(term_name)
        raise Exception(term_name + "not exist")

    def show_buying_policy(self):
        ans = ""
        for t in self.terms_dict:
            ans += self.terms_dict[t][1] + "   "
        return ans
