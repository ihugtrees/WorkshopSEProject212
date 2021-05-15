from OnlineStore.src.domain_layer.user.cart import Cart
from OnlineStore.src.dto.basket_dto import BasketDTO


class CartDTO:
    def __init__(self, cart: Cart):
        self.basket_dict = dict()
        for store_name_key in cart.basket_dict.keys():
            self.basket_dict[store_name_key] = BasketDTO(cart.basket_dict[store_name_key])
        self.sum = 0
