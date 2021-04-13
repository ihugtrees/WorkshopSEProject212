from OnlineStore.src.domain.user.basket import Basket


class Cart:
    def __init__(self):
        self.basket_dict = dict()  # key - store id, value - basket TODO declare type for dict

    def add_product_to_cart(self, product_id, quantity, store_name):
        if store_name not in self.basket_dict.keys():
            new_basket = Basket()
            self.basket_dict[store_name] = new_basket
        self.basket_dict[store_name].add_product(product_id, quantity)

    def remove_product_from_cart(self, product_id, quantity, store_name):
        if store_name not in self.basket_dict.keys():
            raise Exception("wrong store name")
        self.basket_dict[store_name].remove_product(product_id, quantity)



