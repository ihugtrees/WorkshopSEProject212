from OnlineStore.src.domain.user.cart import Cart


class User:
    def __init__(self, user_name: str, cart: Cart, is_admin=False, purchase_history=list()):  # change purchase history from none to empty list (yonatan)
        self.is_logged = False
        self.user_name = user_name
        self.cart = cart
        self.__is_admin = is_admin
        self.purchase_history = purchase_history

    def login(self):
        if self.is_logged:
            raise Exception("Already loggedIn")
        self.is_logged = True

    def logout(self):
        self.is_logged = False

    def is_admin(self):
        return self.__is_admin

    def add_product_to_user(self, store, product_id: int, quantity: int):
        self.cart.add_product_to_cart(store, product_id, quantity)

    def remove_product_from_user(self, store, product_id: int, quantity: int):
        self.cart.remove_product_from_cart(store, product_id, quantity)
