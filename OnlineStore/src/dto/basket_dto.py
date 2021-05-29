from OnlineStore.src.domain_layer.user.basket import Basket


class BasketDTO:
    def __init__(self, basket: Basket):
        self.products_dict = basket.products_dict  # key-product_id , value-quantity
