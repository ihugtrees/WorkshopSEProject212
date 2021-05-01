from OnlineStore.src.domain.user.action import Action
from OnlineStore.src.domain.user.cart import Cart
from OnlineStore.src.domain.user.appoint import *


class User:
    def __init__(self, user_name: str, cart: Cart, is_admin=False,
                 purchase_history=list(), appointed_to_store=None):  # change purchase history from none to empty list (yonatan)
        self.is_logged = False
        self.user_name = user_name
        self.cart = cart
        self.__is_admin = is_admin
        self.purchase_history = purchase_history
        self.appointed_to_store = appointed_to_store if appointed_to_store is not None else Appoint()

    def login(self):
        if self.is_logged:
            raise Exception("Already loggedIn")
        self.is_logged = True

    def logout(self):
        if not self.is_logged:
            raise Exception("Already disconnected")
        self.is_logged = False

    def is_admin(self):
        return self.__is_admin

    def add_product_to_user(self, store, product_id: int, quantity: int):
        self.cart.add_product_to_cart(store, product_id, quantity)

    def remove_product_from_user(self, store, product_id: int, quantity: int):
        self.cart.remove_product_from_cart(store, product_id, quantity)

    def empty_cart(self):
        self.cart = Cart()
    
    def is_assigned_by_me(self, store_manager_name: str, store_name: str)->None:
        self.appointed_to_store.is_appointed_by_me(store_name, store_manager_name)

    def assign_store_employee(self, new_store_owner_name: str, store_name: str)->None:
        self.appointed_to_store.assign_store_employee(new_store_owner_name, store_name)

    def remove_employee(self, store_employee: str, store_name: str)->None:
        self.appointed_to_store.remove_appointed(store_employee, store_name)

    def get_all_appointed(self, store_name: str)->list:
        return self.appointed_to_store.get_all_appointed(store_name)