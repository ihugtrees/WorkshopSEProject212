from OnlineStore.src.domain_layer.user.appoint import *
from OnlineStore.src.domain_layer.user.cart import Cart


class User:
    def __init__(self, user_name: str, cart=None, is_admin=False,
                 purchase_history=None,
                 appointed_to_store=None, guest=True,
                 age=20):
        self.user_name = user_name
        self.is_guest = guest
        self.cart = cart if cart is not None else Cart()
        self.is_admin = is_admin
        self.purchase_history = purchase_history if purchase_history is not None else list()
        self.appointed_to_store = appointed_to_store if appointed_to_store is not None else Appoint()
        self.msgs = None
        self.age = age

    def is_admin(self):
        return self.is_admin

    def is_guest(self):
        return self.is_guest

    def add_product_to_user(self, store, product_id: int, quantity: int):
        self.cart.add_product_to_cart(store, product_id, quantity)

    def remove_product_from_user(self, store, product_id: int, quantity: int):
        self.cart.remove_product_from_cart(store, product_id, quantity)

    def empty_cart(self):
        self.cart = Cart()

    def is_assigned_by_me(self, store_manager_name: str, store_name: str) -> None:
        self.appointed_to_store.is_appointed_by_me(store_name, store_manager_name)

    def assign_store_employee(self, new_store_owner_name: str, store_name: str) -> None:
        self.appointed_to_store.assign_store_employee(new_store_owner_name, store_name)

    def remove_employee(self, store_employee: str, store_name: str) -> None:
        self.appointed_to_store.remove_appointed(store_employee, store_name)

    def get_all_appointed(self, store_name: str) -> list:
        return self.appointed_to_store.get_all_appointed(store_name)

    def remove_store_from_appoint(self, store_name):
        self.appointed_to_store.remove_store_from_appoint(store_name)

    def add_purchase_history(self, receipt):
        self.purchase_history.append(receipt)
