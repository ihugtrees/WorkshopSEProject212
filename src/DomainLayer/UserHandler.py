from src.DomainLayer.User import *


class UserHandler:
    def __init__(self):
        self.users = dict()

    def create_user(self, username, password):
        self.users[username] = User(username, password)

    def print_users(self):
        print(self.users)
