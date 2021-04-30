from OnlineStore.src.domain.store.inventory import Inventory
from OnlineStore.src.domain.user.basket import Basket
from OnlineStore.src.domain.user.user import User


class Store:
    def __init__(self, store_name, store_founder, owners=None, managers=None,
                 buying_policy=None, discount_policy=None, purchase_history=None):
        self.name = store_name
        self.store_founder = store_founder
        self.inventory = Inventory(dict())
        self.buying_policy = buying_policy
        self.discount_policy = discount_policy
        self.purchase_history = purchase_history
        self.rating = 0

    def remove_product_store(self, product_id):
        self.inventory.remove_product_inventory(product_id)

    def add_product_store(self, product_details):
        self.inventory.add_product_inventory(product_details)

    def edit_product(self, product_id, product_details):
        if product_id not in self.inventory.products_dict:
            raise Exception("cant edit non existent product")
        self.inventory.products_dict[product_id].edit_product_description(product_details)

    def is_policies_eligible(self, user: User):  # TODO
        pass

    def calculate_basket_sum(self, basket: Basket) -> int:
        basket_sum = 0
        for product_name in basket.products_dict.keys():
            basket_sum += self.inventory.products_dict.get(product_name).calculate_product_sum(
                basket.products_dict.get(product_name))

        return basket_sum