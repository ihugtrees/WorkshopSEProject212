class Basket:
    def __init__(self):
        self.products = dict()

    def add_product(self, product_id, quantity):
        if quantity <= 0:
            raise Exception("wrong quantity chosen")
        product_quantity = self.products[product_id]
        if product_quantity is None:
            self[product_id] = quantity
        else:
            self[product_id] += quantity

    def remove_product(self, product_id):
        self.product_id_list.remove(product_id)
        return len(self.product_id_list)

    def get_product_list(self):
        return self.product_id_list
