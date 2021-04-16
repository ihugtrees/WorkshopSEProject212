from enum import Enum

from OnlineStore.src.domain.user.cart import Cart
from OnlineStore.src.domain.user.user import User

import random
import string


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
    # print("Random string of length", length, "is:", result_str)


GUEST_NAME_LENGTH = 20


class UserHandler:
    def __init__(self):
        self.users_dict = dict()  # key-user_name, value - user
        # self.data_access = Data()

    def print_users(self):
        print(self.users_dict)

    def register(self, user_name):
        if user_name in self.users_dict:
            raise Exception("user name already exists in the system")
        self.users_dict[user_name] = User(user_name, Cart())
        return True
        user = User(user_name, Cart())
        self.users_dict[user_name] = user
        return user

    def get_cart_info(self, user_name):
        user = self.users_dict[user_name]
        if user is None:
            raise Exception("user name does not exists in the system")
        return user.cart

    def login(self, user_name):
        if user_name not in self.users_dict:
            raise Exception("User does not exist!")
        self.users_dict[user_name].login()
        return True

    def logout(self, user_name):
        if user_name not in self.users_dict or not self.users_dict[user_name].is_logged:
            raise Exception("User does not exist!")
        self.users_dict[user_name].logout()
        # TODO SAVE ALL DATA
        return True

    def exit_the_site(self, guest_name):
        if guest_name not in self.users_dict:
            raise Exception("Guest doesn't exists in the system")
        self.users_dict.pop(guest_name)

    def add_product(self, user_name, store_id, product_id, quantity):
        if user_name not in self.users_dict:
            raise Exception("User does not exist!")
        self.users_dict[user_name].add_product_to_user(store_id, product_id, quantity)

    def remove_product(self, user_name, store_id, product_id, quantity):
        if user_name not in self.users_dict:
            raise Exception("user name does not exists in the system")
        self.users_dict[user_name].remove_product_from_user(store_id, product_id, quantity)

    def get_cart(self, user_name):
        if user_name not in self.users_dict:
            raise Exception("user name does not exists in the system")
        return self.users_dict[user_name].cart

    # def load_users(self):
    #     self.users_dict = data_access.load_users()

    def get_guest_unique_user_name(self):
        new_user_name = get_random_string(GUEST_NAME_LENGTH)
        while new_user_name in self.users_dict:
            new_user_name = get_random_string(GUEST_NAME_LENGTH)
        self.users_dict[new_user_name] = User(new_user_name, Cart())
        return new_user_name

    def check_permission_to_open_store(self, user_name):
        user = self.users_dict.get(user_name)
        if user is None:
            raise Exception("user name does not exists in the system")
        if user.is_logged is False:
            raise Exception("the current user is not logged in, so he cannot open a store")

    def get_user_purchase_history(self, user_name):
        user = self.users_dict[user_name]
        if user is None:
            raise Exception("user name does not exists in the system")
        return user.purchase_history

    def edit_store_manager_permissions(self, user_name, store_manager_name: str, new_permissions: int):
        user = self.users_dict.get(store_manager_name)
        if user is None:
            raise Exception("Store manager does not exists in the system")
        user.edit_store_manager_permissions(new_permissions)

    def is_permitted_to_do(self, user_name: str, store_name: str, action: int):
        user = self.users_dict.get(user_name)
        if user is None:
            raise Exception("The user does not exists in the system")
        user.is_permitted_to_do(action, store_name)

    def get_employee_information(self, employee_name):
        user = self.users_dict.get(employee_name)
        if user is None:
            raise Exception("The Employee user does not exists in the system")
        return user #TODO WHAT TO RETURN?? WHICH FIELDS?


class Action(Enum):
    EMPLOYEE_INFO = 0
    EMPLOYEE_PERMISSIONS = 1
