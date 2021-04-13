from OnlineStore.src.domain.user.cart import Cart


class User:
    def __init__(self, user_name, cart: Cart, is_guest=True, purchase_history=None):
        self.logged_in = False
        self.user_name = user_name
        self.cart = cart
        self.is_guest = is_guest
        self.purchase_history = purchase_history

    def login(self):
        self.logged_in = True

    def logout(self):
        self.logged_in = False

    def add_product_to_user(self, store, product_id: int, quantity: int):
        self.cart.add_product_to_cart(store, product_id, quantity)

    def remove_product_from_user(self, store, product_id: int, quantity: int):
        self.cart.remove_product_from_cart(store, product_id, quantity)
