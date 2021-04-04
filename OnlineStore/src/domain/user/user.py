from OnlineStore.src.domain.user.cart import Cart


class User:
    def __init__(self, cart: Cart):
        self.cart = cart
        # self.user_id = user_id
        if type(self) is User:
            raise Exception('Base is an abstract class and cannot be instantiated directly')

    def add_product_to_cart(self, product_id: int, store_id: int):
        self.cart.add_product_to_Cart(product_id, store_id)

    def remove_product_from_cart(self, product_id: int, store_id: int):
        self.Cart.remove_product_from_cart(product_id, store_id)
