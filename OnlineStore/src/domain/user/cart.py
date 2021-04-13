from OnlineStore.src.domain.user.basket import Basket


class Cart:
    def __init__(self):
        self.basketList = dict() # key - store id, value - basket TODO declare type for dict

    def add_product_to_cart(self, product_id, store_id, quantity):
        if store_id not in self.basketList.keys():
            new_basket = Basket()
            self.basketList[store_id] = new_basket
        self.basketList[store_id].add_product(product_id, quantity)

    def remove_product_from_cart(self, product_id: int, store_id: int):
        if self.basketList[store_id].remove(product_id) == 0:
            self.basketList.pop(store_id)



