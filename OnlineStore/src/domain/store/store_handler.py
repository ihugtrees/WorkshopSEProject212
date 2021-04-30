from OnlineStore.src.domain.store.store import Store
from OnlineStore.src.domain.user.cart import Cart
from OnlineStore.src.domain.user.user import User
import OnlineStore.src.data_layer.purchase_data as purchase_handler
from OnlineStore.src.domain.store.purchase import Purchase
import random
import string

from OnlineStore.src.dto.cart_dto import CartDTO
from OnlineStore.src.dto.user_dto import UserDTO


class StoreHandler:

    def __init__(self):
        self.store_dict = dict()  # key-store name, value-store

    def get_random_string(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str
        # print("Random string of length", length, "is:", result_str)

    def open_store(self, store_name, founder):
        if store_name in self.store_dict:
            raise Exception("store name already exists in the system")
        self.store_dict[store_name] = Store(store_name=store_name, store_founder=founder)

    def add_new_product_to_store_inventory(self, user_name, product_details, store_name):
        store = self.store_dict.get(store_name)
        if store is None:
            raise Exception("store name does not exists in the system")
        if store.inventory.products_dict.get(product_details["product_id"]) is not None:
            raise Exception("product id already exists in the store")
        store.add_product_store(product_details)

    def remove_product_from_store_inventory(self, user_name, product_id, store_name):
        store = self.store_dict.get(store_name)
        if store is None:
            raise Exception("The store does not exists in the system")
        store.remove_product_store(product_id)

    def get_information_about_products(self, store_name):
        if store_name not in self.store_dict:
            raise Exception("store name does not exists in the system")
        return self.store_dict[store_name].inventory.products_dict

    def get_store_info(self, store_name):
        store = self.store_dict.get(store_name)
        if store is None:
            raise Exception("store name does not exists in the system")
        return {"store_name": store.name, "store_founder": store.store_founder,
                "buying_policy": store.buying_policy, "discount_policy": store.discount_policy}

    def get_store(self, store_name):
        store = self.store_dict.get(store_name)
        if store is None:
            raise Exception("store name does not exists in the system")
        return store

    def check_product_exists_in_store(self, product_id, store_name):
        store = self.store_dict.get(store_name)
        if store is None:
            raise Exception("store name does not exists in the system")
        if not (product_id in store.inventory.products_dict):
            raise Exception("product id does not exists in the store")
        if store.inventory.products_dict[product_id].quantity <= 0:
            raise Exception("product quantity is less than 1")

    def find_product_by_id(self, product_id, store_name):
        store = self.store_dict.get(store_name)
        if store is None:
            raise Exception("The store does not exists in the system")
        product = store.inventory.products_dict.get(product_id)
        if product is None:
            raise Exception("Product does not exist in the store")
        return product

    def get_store_purchase_history(self, store_name):
        store = self.store_dict.get(store_name)
        if store is None:
            raise Exception("The store does not exists in the system")
        return store.purchase_history

    def __get_stores_from_cart(self, cart: Cart):
        stores = list()
        for store_name in cart.basket_dict.keys():
            stores.append(self.get_store(store_name))
        return stores

    def is_valid_for_purchase(self, cart: CartDTO, user: UserDTO):
        for store in self.__get_stores_from_cart(cart):
            store.is_policies_eligible(user)

    def take_quantity(self, cart: CartDTO):
        for store in self.__get_stores_from_cart(cart):
            store.inventory.take_quantity(cart.basket_dict.get(store.name))

    def calculate_cart_sum(self, cart: CartDTO) -> int:
        money_sum = 0
        for store in self.__get_stores_from_cart(cart):
            money_sum += store.calculate_basket_sum(cart.basket_dict.get(store.name))
        return money_sum

    def add_all_basket_purchases_to_history(self, cart: CartDTO, user_name):
        for store_name in cart.basket_dict.keys():
            while True:
                try:
                    purchase_handler.add_purchase(Purchase(self.get_random_string(20), user_name, store_name))
                    break
                except:
                    continue
