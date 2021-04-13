from OnlineStore.src.domain.user.cart import Cart


class User:
    def __init__(self, user_name, password, cart: Cart, first_name, last_name, birthdate, is_guest):
        self.loggedIn = False
        self.user_name = user_name
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.cart = cart
        self.is_guest = is_guest

    def login(self, password):
        if password is not self.password:
            raise Exception("The password is incorrect")
        self.loggedIn = True
