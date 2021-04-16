from OnlineStore.src.domain.store.product import Product


class Inventory:
    def __init__(self):
        self.products_dict = dict()

    def remove_product_inventory(self, product_id):
        if self.products_dict.get(product_id) is None:
            raise Exception("Product does not exist in the store")
        self.products_dict.pop(product_id)

    def add_product_inventory(self, product_details):
        if product_details["product_id"] in self.products_dict:
            raise Exception("Product already exist in the store")
        self.products_dict[product_details["product_id"]] = Product(product_details["product_id"],
                                                                    product_details["product_name"],
                                                                    product_details["quantity"])
