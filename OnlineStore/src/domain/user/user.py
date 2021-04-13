from OnlineStore.src.domain.user.cart import Cart


class User:
    def __init__(self, user_name, password, cart: Cart, first_name, last_name, birthdate, is_guest, purchase_history):
        self.loggedIn = False
        self.user_name = user_name
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.cart = cart
        self.is_guest = is_guest
        self.purchase_history = purchase_history

    def login(self, password):
        if password is not self.password:
            raise Exception("The password is incorrect")
        self.loggedIn = True

    def add_product_to_cart(self, product_id: int, store_id: int):
        self.cart.add_product_to_Cart(product_id, store_id)

    def remove_product_from_cart(self, product_id: int, store_id: int):
        self.Cart.remove_product_from_cart(product_id, store_id)

    def logout(self):
        self.loggedIn = False
