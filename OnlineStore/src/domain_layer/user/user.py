from OnlineStore.src.domain_layer.user.appoint import *
from OnlineStore.src.domain_layer.user.cart import Cart
import OnlineStore.src.data_layer.users_data as users


class User:
    def __init__(self, user_name: str, cart=None, is_admin=False,
                 appointed_to_store=None, guest=True,
                 age=20):
        self.user_name = user_name
        self.is_guest = guest
        self.cart = cart if cart is not None else Cart()
        self.is_admin = is_admin
        self.appointed_to_store = appointed_to_store if appointed_to_store is not None else Appoint()
        self.age = age

    def add_product_to_user(self, store, product_id: int, quantity: int):
        self.cart.add_product_to_cart(store, product_id, quantity)

    def remove_product_from_user(self, store, product_id: int, quantity: int):
        self.cart.remove_product_from_cart(store, product_id, quantity)

    def empty_cart(self):
        self.cart = Cart()

    def is_assigned_by_me(self, store_manager_name: str, store_name: str) -> None:
        users.get_appoint_by_user(self.user_name).is_appointed_by_me(store_name, store_manager_name)

    def assign_store_employee(self, new_store_owner_name: str, store_name: str) -> None:
        # users.get_appoint_by_user(self.user_name).assign_store_employee(new_store_owner_name, store_name)
        users.add_appointee(self.user_name, new_store_owner_name, store_name)

    def remove_employee(self, store_employee: str, store_name: str) -> None:
        users.get_appoint_by_user(self.user_name).remove_appointed(store_employee, store_name)

    def get_all_appointed(self, store_name: str) -> list:
        return users.get_appoint_by_user(self.user_name).get_all_appointed(store_name)

    def remove_store_from_appoint(self, store_name):
        users.get_appoint_by_user(self.user_name).remove_store_from_appoint(store_name)
