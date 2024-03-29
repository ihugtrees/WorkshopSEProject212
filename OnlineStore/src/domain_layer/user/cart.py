from OnlineStore.src.domain_layer.user.basket import Basket


class Cart:
    def __init__(self):
        self.basket_dict = dict()  # key - store id, value - basket TODO declare type for dict

    def add_product_to_cart(self, store_name, product_id, quantity):
        if store_name not in self.basket_dict:
            self.basket_dict[store_name] = Basket()
        self.basket_dict[store_name].add_product_to_basket(product_id, quantity)

    def remove_product_from_cart(self, store_name, product_id, quantity):
        if store_name not in self.basket_dict:
            raise Exception("wrong store name")
        self.basket_dict[store_name].remove_product_from_basket(product_id, quantity)
        if len(self.basket_dict[store_name].products_dict) == 0:
            self.basket_dict.pop(store_name)

    def get_str_cart(self):
        output = ""
        for id in self.basket_dict:
            output = output+"Store ID : "+id+"\n"+self.basket_dict[id].get_str_basket(self)
        return ""

