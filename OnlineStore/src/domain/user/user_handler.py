from OnlineStore.src.domain.user.user import *

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
        self.users_dict = dict() # key-user_name, value - user

    def print_users(self):
        print(self.users_dict)

    def login(self, user_name, password):
        user = self.users_dict.users[user_name]
        if user is None:
            raise Exception("User does not exist!")
        user.login(password)

    def get_guest_unique_user_name(self):
        guest = None
        while guest is None:
            new_user_name = get_random_string(GUEST_NAME_LENGTH)
            guest = self.users_dict.get(new_user_name)
        self.users_dict[guest] = User(new_user_name, None, Cart(), "guest", "guest", None, True)
        return new_user_name

    def exit_the_site(self, guest_name):
        if self.users_dict.pop(guest_name) is None:
            raise Exception("Guest doesn't exists in the system")

    def register(self, user_name, password, first_name, last_name, birthdate):
        if self.users_dict[user_name] is None:
            raise Exception("user name already exists in the system")
        self.users_dict[user_name] = User(user_name, password, Cart(), first_name, last_name, birthdate, False)

    def get_cart_info(self, user_name):
        user = self.users_dict[user_name]
        if user is None:
            raise Exception("user name does not exists in the system")
        return user.cart.basketList

    def add_product(self, user_name, product_id, quantity, store_id):
        user = self.users_dict[user_name]
        if user is None:
            raise Exception("user name does not exists in the system")
        return user.cart.add_product_to_cart(product_id, quantity, store_id)




