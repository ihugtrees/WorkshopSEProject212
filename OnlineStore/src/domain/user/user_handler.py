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
    id_counter = 0 # every new user get the counter and the counter inc
    def __init__(self):
        self.users_dict = dict[str, User] # key-user_name, value - user

    def create_user(self, username):

        self.users_dict[username] = User()

    def print_users(self):
        print(self.users_dict)

    def login(self, user_name, password):
        user = self.users_dict.users.get(user_name)
        if user is None:
            raise Exception("User does not exist!")
        user.login(password)

    def get_guest_unique_user_name(self):
        guest = None
        while guest is None:
            new_user_name = get_random_string(GUEST_NAME_LENGTH)
            guest = self.users_dict.get(new_user_name)
        self.users_dict[guest] = User(new_user_name, None, Cart(), True)
        return new_user_name

    def exit_the_site(self, guest_name):
        if self.users_dict.pop(guest_name) is None:
            raise Exception("Guest doesn't exists in the system")


