from threading import Lock

from OnlineStore.src.domain_layer.store.product import Product
from OnlineStore.src.domain_layer.user.basket import Basket


class Inventory:
    def __init__(self, products_dict):
        self.products_dict = products_dict  # {String: Product}
        self.lock = Lock()

    def remove_product_inventory(self, product_id):
        if self.products_dict.get(product_id) is None:
            raise Exception("Product does not exist in the store")
        self.products_dict.pop(product_id)

    def add_product_inventory(self, product_details):
        self.lock.acquire()
        if product_details["product_id"] in self.products_dict:
            self.lock.release()
            raise Exception("Product already exist in the store")
        self.products_dict[product_details["product_id"]] = Product(product_details["product_id"],
                                                                    product_details["product_name"],
                                                                    product_details["quantity"],
                                                                    product_details["price"])
        self.lock.release()

    def take_quantity(self, basket: Basket):
        exception_string = ""
        self.lock.acquire()
        for product_name in basket.products_dict.keys():
            try:
                self.products_dict.get(product_name).take_quantity(
                    basket.products_dict.get(product_name))
            except Exception as e:
                exception_string += e.args[0]

        if exception_string != "":
            self.__rollback_from_take_quantity(basket)
            self.lock.release()
            raise Exception(exception_string)
        self.lock.release()

    def return_quantity(self, basket: Basket):
        exception_string = ""
        for product_name in basket.products_dict.keys():
            try:
                self.products_dict.get(product_name).return_quantity(
                    basket.products_dict.get(product_name))
            except Exception as e:
                exception_string += e.args[0]

    def __rollback_from_take_quantity(self, basket):
        for product_name in basket.products_dict.keys():
            try:
                self.products_dict.get(product_name).take_quantity(
                    basket.products_dict.get(product_name))
                self.products_dict.get(product_name).add_quantity(basket.products_dict.get(product_name) * 2)
            except Exception as e:
                None
