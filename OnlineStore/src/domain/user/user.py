from OnlineStore.src.domain.user.cart import Cart


class User:
    def __init__(self, user_name, password, cart: Cart, is_guest):
        self.loggedIn = False
        self.user_name = user_name
        self.password = password
        self.cart = cart
        self.is_guest = is_guest

    def login(self, password):
        if password is not self.password:
            raise Exception("The password is incorrect")
        self.loggedIn = True