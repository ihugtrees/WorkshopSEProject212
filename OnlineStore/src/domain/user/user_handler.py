from OnlineStore.src.domain.user.user import *


class UserHandler:
    id_counter = 0 # every new user get the counter and the counter inc
    def __init__(self):
        self.users_dict = dict[int, User] # key-id, value - user

    def create_user(self, username):

        self.users_dict[username] = User()

    def print_users(self):
        print(self.users_dict)


