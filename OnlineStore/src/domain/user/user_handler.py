from OnlineStore.src.domain.user.user import *


class UserHandler:
    def __init__(self):
        self.users = dict()

    def create_user(self, username):
        self.users[username] = User()

    def print_users(self):
        print(self.users)

   # def add_product_to_cart(self, ):
