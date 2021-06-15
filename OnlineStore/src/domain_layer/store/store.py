from OnlineStore.src.domain_layer.store.buying_offer import BuyingOffer
from OnlineStore.src.domain_layer.store.buying_policy.buying_policy import BuyingPolicy
from OnlineStore.src.domain_layer.store.discont_policy.discount_policy import DiscountPolicy
from OnlineStore.src.domain_layer.store.inventory import Inventory
from OnlineStore.src.domain_layer.user.basket import Basket
from OnlineStore.src.dto.user_dto import UserDTO


class Store:
    def __init__(self, store_name, store_founder,
                 buying_policy=None, discount_policy=None):
        self.name = store_name
        self.store_founder = store_founder
        self.inventory = Inventory(dict())
        self.rating = 0
        self.buying_policy: BuyingPolicy = buying_policy if buying_policy is not None else BuyingPolicy()
        self.discount_policy = discount_policy if discount_policy is not None else DiscountPolicy()
        self.buying_offers = dict()   # key product_name val BuyingOffer

    def remove_product_store(self, product_id, store):
        self.inventory.remove_product_inventory(product_id, store)

    def add_product_store(self, product_details):
        self.inventory.add_product_inventory(product_details)

    def edit_product(self, product_id, product_details):
        if product_id not in self.inventory.products_dict:
            raise Exception("cant edit non existent product")
        self.inventory.products_dict[product_id].edit_product_details(product_details, self.name)

    def is_policies_eligible(self, user: UserDTO) -> None:
        if self.buying_policy is not None:
            user_data = self.make_user_data_from_user_dto(user)
            basket_data = self.make_basket_dto_from_basket(user.cart.basket_dict[self.name])
            self.buying_policy.eligible_for_buying(user, basket_data)  # TODO changed from user_data->user

    def calculate_basket_sum(self, basket: Basket) -> int:  # basketDTO???
        if self.discount_policy is not None:
            basket_data = self.make_basket_dto_from_basket(basket)
            price = self.discount_policy.calc_price(basket_data)
            if price != -1:
                return price

        basket_sum = 0
        for product_name in basket.products_dict.keys():
            basket_sum += self.inventory.products_dict.get(product_name) \
                .calculate_product_sum(basket.products_dict.get(product_name))
        return basket_sum

    def make_basket_dto_from_basket(self, basket: Basket):  # product_name -> (quantity, price ,category)
        dict_ans = dict()
        for p in basket.products_dict:
            product = self.inventory.products_dict[p]
            quantity = basket.products_dict[p]
            price = product.price
            category = product.category
            dict_ans[p] = (quantity, price, category)
        return dict_ans

    def add_discount(self, discount_name: str, discount_value: str, discount_term: str = None,
                     discount_value_type: str = False, store= None):
        self.discount_policy.add_discount(discount_name, discount_value, discount_term=discount_term,
                                          discount_value_type=discount_value_type, store=store)

    def combine_discount(self, d1_name, d2_name, operator: str, new_name):
        self.discount_policy.combine_discount(d1_name, d2_name, operator, new_name)

    def show_discount(self):
        return self.discount_policy.show_discount_policy()

    def delete_discount(self, discount_name):
        return self.discount_policy.delete_discount(discount_name)

    def add_buying_policy(self, policy_name: str, s_term: str, no_flag=False):
        self.buying_policy.add_buying_term(policy_name, s_term, no_flag=no_flag, store=self.name)

    def open_product_to_offer(self, product_name, minimum):
        b = BuyingOffer(product_name, minimum)
        if product_name in self.buying_offers:
            raise Exception("the product already in type offer")
        if product_name not in self.inventory.products_dict:
            raise Exception("the product not in store")
        self.buying_offers[product_name] = b

    def make_offer(self, user_name, product_name, quantity, price, payment_detial, buyer_information):
        if product_name not in self.buying_offers:
            raise Exception("the product not open for offers")
        if quantity > self.inventory.products_dict[product_name].quantity:
            raise Exception("no such quantity")
        if price < self.buying_offers[product_name].minimum:
            raise Exception("the minimum price is: " + str(self.buying_offers[product_name].minimum))
        self.buying_offers[product_name].offers[user_name] = (quantity, price)
        self.buying_offers[product_name].payment_detial[user_name] = payment_detial
        self.buying_offers[product_name].buyer_information[user_name] = buyer_information
        self.buying_offers[product_name].all_acceptance[user_name] = set()


    def delete_buying_policy(self, term_name):
        self.buying_policy.delete_buying_term(term_name)

    def show_buying_policy(self):
        return self.buying_policy.show_buying_policy()

    def make_user_data_from_user_dto(self, user_dto: UserDTO):
        ans = dict()
        ans["age"] = user_dto.age
        ans["user_name"] = user_dto.user_name
        return ans

    def accept_offer(self, product_name, user_name, owner_name, num_of_acceptance):
        if product_name not in self.buying_offers:
            raise Exception(product_name + " is not for offers")
        if user_name not in self.buying_offers[product_name].offers:
            raise Exception(user_name + " does not have offer")
        if owner_name in self.buying_offers[product_name].all_acceptance:
            raise Exception("yoe already accept")
        self.buying_offers[product_name].all_acceptance[user_name].add(owner_name)
        price = self.buying_offers[product_name].offers[user_name][1]
        quantity = self.buying_offers[product_name].offers[user_name][0]
        if len(self.buying_offers[product_name].all_acceptance[user_name]) == num_of_acceptance:
            payment_info = self.buying_offers[product_name].payment_detial[user_name]
            buyer_info = self.buying_offers[product_name].buyer_information[user_name]
            self.buying_offers[product_name].offers.pop(user_name)
            self.buying_offers[product_name].all_acceptance.pop(user_name)
            self.buying_offers[product_name].buyer_information.pop(user_name)
            self.buying_offers[product_name].payment_detial.pop(user_name)
            return payment_info, buyer_info, quantity, price

    def reject_offer(self, user_name, product_name):
        if product_name not in self.buying_offers:
            raise Exception(product_name + " is not for offers")
        if user_name not in self.buying_offers[product_name].offers:
            raise Exception(user_name + " does not have offer")
        self.buying_offers[product_name].offers.pop(user_name)

