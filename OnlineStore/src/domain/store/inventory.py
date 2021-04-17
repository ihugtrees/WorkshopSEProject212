from OnlineStore.src.domain.store.product import Product
from OnlineStore.src.domain.user.basket import Basket


class Inventory:
    def __init__(self, products_dict):
        self.products_dict = products_dict

    def remove_product_inventory(self, product_id):
        if self.products_dict.get(product_id) is None:
            raise Exception("Product does not exist in the store")
        self.products_dict.pop(product_id)

    def add_product_inventory(self, product_details):
        if product_details["product_id"] in self.products_dict:
            raise Exception("Product already exist in the store")
        self.products_dict[product_details["product_id"]] = Product(product_details["product_id"],
                                                                    product_details["product_name"],
                                                                    product_details["quantity"],
                                                                    product_details["price"])

    def take_quantity(self, basket: Basket):
        exception_string = ""
        for product_name in basket.products_dict.keys():
            try:
                self.products_dict.get(product_name).take_quantity(
                    basket.products_dict.get(product_name))
            except Exception as e:
                exception_string += e.args[0]

        if exception_string != "":
            self.__rollback_from_take_quantity(basket)
            raise Exception(exception_string)

    def __rollback_from_take_quantity(self, basket):
        for product_name in basket.products_dict.keys():
            try:
                self.products_dict.get(product_name).take_quantity(
                    basket.products_dict.get(product_name))
                self.products_dict.get(product_name).add_quantity(basket.products_dict.get(product_name) * 2)
            except Exception as e:
                None
