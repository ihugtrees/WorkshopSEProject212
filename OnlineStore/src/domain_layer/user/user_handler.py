import random
import string
from threading import Lock

import OnlineStore.src.data_layer.permissions_data as permissions
import OnlineStore.src.data_layer.users_data as users
from OnlineStore.src.domain_layer.user.action import *
from OnlineStore.src.domain_layer.user.cart import Cart
from OnlineStore.src.domain_layer.user.user import User
from OnlineStore.src.dto.cart_dto import CartDTO
from OnlineStore.src.dto.user_dto import UserDTO


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


GUEST_NAME_LENGTH = 20


class UserHandler:
    def __init__(self):
        self.users_dict = dict()  # key-user_name, value - user
        self.lock = Lock()

    def print_users(self):
        print(self.users_dict)

    def register(self, user_name, age):
        self.lock.acquire()
        user = User(user_name, Cart(), guest=False)
        try:
            users.add_user(user)
            permissions.add_permission(user_name, REGISTERED_PERMMISIONS)
            self.lock.release()
        except Exception as e:
            self.lock.release()
            raise e

    def get_cart_info(self, user_name) -> CartDTO:
        user = users.get_user_by_name(user_name)
        return CartDTO(user.cart)

    def login(self, user_name):
        users.get_user_by_name(user_name).login()

    def logout(self, user_name):
        users.get_user_by_name(user_name).logout()

    def exit_the_site(self, guest_name):
        users.remove_user(guest_name)

    def add_product(self, user_name, store_id, product_id, quantity):
        users.get_user_by_name(user_name).add_product_to_user(store_id, product_id, quantity)

    def remove_product(self, user_name, store_id, product_id, quantity):
        users.get_user_by_name(user_name).remove_product_from_user(store_id, product_id, quantity)

    def get_guest_unique_user_name(self):
        new_user_name = get_random_string(GUEST_NAME_LENGTH)
        while True:
            new_user_name = get_random_string(GUEST_NAME_LENGTH)
            try:
                users.add_user(User(new_user_name, 0, Cart()))
                break
            except:
                continue
        return new_user_name

    def check_permission_to_open_store(self, user_name):
        user = users.get_user_by_name(user_name)
        if user.is_logged is False:
            raise Exception("the current user is not logged in, so he cannot open a store")

    def get_user_purchase_history(self, user_name):
        user = users.get_user_by_name(user_name)
        return user.purchase_history

    def get_employee_information(self, employee_name: str):
        return self.get_user_dto_by_name(employee_name)

    def get_user_dto_by_name(self, user_name) -> UserDTO:
        return UserDTO(users.get_user_by_name(user_name))

    def empty_cart(self, user_name):
        users.get_user_by_name(user_name).empty_cart()

    def is_assigned_by_me(self, user_name: str, store_manager_name: str, store_name: str) -> None:
        users.get_user_by_name(user_name).is_assigned_by_me(store_manager_name, store_name)

    def assign_store_employee(self, user_name: str, new_store_owner_name: str, store_name: str) -> None:
        users.get_user_by_name(user_name).assign_store_employee(new_store_owner_name, store_name)

    def remove_employee(self, user_name: str, store_employee: str, store_name: str) -> list:
        self.is_assigned_by_me(user_name, store_employee, store_name)
        employee: User = users.get_user_by_name(store_employee)
        to_remove: list = employee.get_all_appointed(store_name)
        users.get_user_by_name(user_name).remove_employee(store_employee, store_name)
        ls: list = self.__remove_employee_rec(to_remove, store_name)
        employee.remove_store_from_appoint(store_name)
        ls.append(store_employee)
        return ls

    def __remove_employee_rec(self, store_employee_list: list, store_name):
        list_em: list = list()
        list_em.extend(store_employee_list)
        for employee_name in store_employee_list:
            list_em.extend(
                self.__remove_employee_rec(users.get_user_by_name(employee_name).get_all_appointed(store_name),
                                           store_name))
            users.get_user_by_name(employee_name).remove_store_from_appoint(store_name)
        return list_em

    def is_user_guest(self, user_name):
        return users.get_user_by_name(user_name).is_guest()
