from OnlineStore.src.domain.user.user_handler import *


def main():
    user_handler = UserHandler()
    user_handler.create_user("abc", "123")
    user_handler.print_users()


main()
