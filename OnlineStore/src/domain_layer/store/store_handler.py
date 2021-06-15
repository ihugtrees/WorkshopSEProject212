import random
import string
from threading import Lock

from pony.orm import db_session

import OnlineStore.src.data_layer.store_data as stores
from OnlineStore.src.domain_layer.store.store import Store
from OnlineStore.src.domain_layer.user.cart import Cart
from OnlineStore.src.dto.cart_dto import CartDTO
from OnlineStore.src.dto.product_dto import ProductDTO
from OnlineStore.src.dto.user_dto import UserDTO


class StoreHandler:
    def __init__(self):
        self.lock = Lock()

    def get_random_string(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str
        # print("Random string of length", length, "is:", result_str)

    def open_store(self, store_name, founder):
        store: Store = Store(store_name=store_name, store_founder=founder)
        self.lock.acquire()
        try:
            stores.add_store(store)
            self.lock.release()
        except Exception as e:
            self.lock.release()
            raise e

    def add_new_product_to_store_inventory(self, user_name, product_details, store_name):
        store: Store = stores.get_store_by_name(store_name)
        if store.inventory.products_dict.get(product_details["product_id"]) is not None:
            raise Exception("product id already exists in the store")
        store.add_product_store(product_details)
        stores.add_product_to_store(store_name, product_details)

    def remove_product_from_store_inventory(self, user_name, product_id, store_name):
        store: Store = stores.get_store_by_name(store_name)
        store.remove_product_store(product_id, store_name)
        stores.remove_product_from_store(store_name, product_id)

    def get_information_about_products(self, store_name):
        store: Store = stores.get_store_by_name(store_name)
        return store.inventory.products_dict

    def get_store_info(self, store_name):
        store: Store = stores.get_store_by_name(store_name)
        store_info = {"Store name:": store.name, "Founder": store.store_founder, "Rating:": store.rating}
        return store_info

    def get_store(self, store_name):
        store: Store = stores.get_store_by_name(store_name)
        return store

    def check_product_exists_in_store(self, product_id, store_name):
        store: Store = stores.get_store_by_name(store_name)
        if not (product_id in store.inventory.products_dict):
            raise Exception("product id does not exists in the store")
        if store.inventory.products_dict[product_id].quantity <= 0:
            raise Exception("product quantity is less than 1")

    def find_product_by_id(self, product_id, store_name):
        store: Store = stores.get_store_by_name(store_name)
        product = store.inventory.products_dict.get(product_id)
        if product is None:
            raise Exception("Product does not exist in the store")
        return product

    def __get_stores_from_cart(self, cart: Cart):
        stores = list()
        for store_name in cart.basket_dict.keys():
            stores.append(self.get_store(store_name))
        return stores

    def is_valid_for_purchase(self, cart: CartDTO, user: UserDTO):
        ans = True
        for store in self.__get_stores_from_cart(cart):
            ans = ans and store.is_policies_eligible(user)
        return ans

    def take_quantity(self, cart: CartDTO):
        for store in self.__get_stores_from_cart(cart):
            store.inventory.take_quantity(cart.basket_dict.get(store.name), store.name)

    def take_quantity_from_store(self, store, product, quantity):
        stores.get_store_by_name(store).inventory.take_quantity_for_one_product(product, quantity, store)

    @db_session
    def return_quantity(self, cart: CartDTO):
        for store in self.__get_stores_from_cart(cart):
            store.inventory.return_quantity(cart.basket_dict.get(store.name), store.name)

    def calculate_cart_sum(self, cart: CartDTO) -> int:
        money_sum = 0
        for store in self.__get_stores_from_cart(cart):
            money_sum += store.calculate_basket_sum(cart.basket_dict.get(store.name))
        return money_sum

    def get_stores_with_rating(self, rating):
        if rating is None:
            rating = 0
        return stores.get_all_stores(rating)

    def get_products_with_filters(self, store, filters):
        """
        filters =
        {min: int/none, max: int/none, prating: int/none, category: str/none, srating: int/none}
        """
        min_price = 0
        rating = 0
        cat = ''

        if filters['min'] is not None:
            min_price = filters['min']
        if filters['prating'] is not None:
            rating = filters['prating']
        if filters['category'] is not None:
            cat = filters['category']

        product_list = list()
        if filters['max'] is not None:
            for key, product in stores.get_store_by_name(store).inventory.products_dict.items():
                if min_price <= product.price <= filters['max'] and rating <= product.rating and product.category.find(
                        cat) != -1:
                    product_list.append(product)
        else:
            for key, product in stores.get_store_by_name(store).inventory.products_dict.items():
                if min_price <= product.price and rating <= product.rating and product.category.find(cat) != -1:
                    product_list.append(product)
        return product_list

    def search_product_by_category(self, category, filters):
        if filters['category'] is not None and category.find(filters['category']) == -1:
            return [False, "category doesnt match"]
        product_list = list()
        for store in self.get_stores_with_rating(filters['srating']):
            for product in self.get_products_with_filters(store.name, filters):
                if product.category.find(category) != -1:
                    product_list.append(vars(ProductDTO(product)))
        if len(product_list) == 0:
            raise Exception("no product found")
        return product_list

    def search_product_by_name(self, name, filters):
        product_list = list()
        for store in self.get_stores_with_rating(filters['srating']):
            for product in self.get_products_with_filters(store.name, filters):
                if product.product_name.find(name) != -1:
                    product_list.append(vars(ProductDTO(product)))
        if len(product_list) == 0:
            raise Exception("no product found")
        return product_list

    def search_product_by_keyword(self, keyword, filters):
        product_list = list()
        for store in self.get_stores_with_rating(filters['srating']):
            for product in self.get_products_with_filters(store.name, filters):
                if product.description.find(keyword) != -1:
                    product_list.append(vars(ProductDTO(product)))
        if len(product_list) == 0:
            raise Exception("no product found")
        return product_list

    def add_discount(self, store, discount_name, discount_value, discount_term=None):
        return stores.get_store_by_name(store).add_discount(discount_name, discount_value, discount_term=discount_term, store=store)

    def combine_discount(self, store, d1_name, d2_name, operator: str, new_name):
        return stores.get_store_by_name(store).combine_discount(d1_name, d2_name, operator, new_name)

    def show_discount_policy(self, store):
        return stores.get_store_by_name(store).show_discount()

    def delete_discount(self, store, discount_name):
        return stores.get_store_by_name(store).delete_discount(discount_name)

    def add_policy(self, store, policy_name: str, s_term: str, no_flag=False):
        ans = stores.get_store_by_name(store).add_buying_policy(policy_name, s_term, no_flag=no_flag)
        stores.add_buying_policy(store, policy_name, s_term)

    def open_product_to_offer(self, store, product_name, minimum):
        return stores.get_store_by_name(store).open_product_to_offer(product_name, minimum)

    def make_offer(self, user_name, store, product_name , quantity, price, payment_detial, buyer_information):
        return stores.get_store_by_name(store).make_offer(user_name, product_name, quantity, price, payment_detial, buyer_information)

    def delete_buying_policy(self, store, policy_name):
        return stores.get_store_by_name(store).delete_buying_policy(policy_name)

    def show_buying_policy(self, store):
        return stores.get_store_by_name(store).show_buying_policy()

    def accept_offer(self, store, product_name, user_name, owner_name, num_of_acceptance):
        return stores.get_store_by_name(store).accept_offer(product_name, user_name, owner_name, num_of_acceptance)

    def reject_offer(self, store, user_name, product_name):
        return stores.get_store_by_name(store).reject_offer(user_name, product_name)