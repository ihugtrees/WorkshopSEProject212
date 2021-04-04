from OnlineStore.src.domain.user.basket import Basket


class Cart:
    def __init__(self):
        self.basketList = dict() # key - store id, value - basket TODO declare type for dict

    def add_product_to_Cart(self, product_id: int, store_id: int):
        if store_id in self.basketList.keys():
            self.basketList[store_id].add_product(product_id)
        else:
            new_basket = Basket()
            new_basket.add_product(product_id)
            self.basketList[store_id] = new_basket



    def remove_product_from_cart(self, product_id: int, store_id: int):
        if self.basketList[store_id].remove(product_id) == 0:
            self.basketList.pop(store_id)



