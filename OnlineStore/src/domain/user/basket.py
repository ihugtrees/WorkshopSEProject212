class Basket:
    def __init__(self):
        self.products = dict()  # key-product_id , value-quantity

    def add_product(self, product_id, quantity):
        if quantity <= 0:
            raise Exception("wrong quantity chosen")
        product_quantity = self.products[product_id]
        if product_quantity is None:
            self.products[product_id] = quantity
        else:
            self.products[product_id] += quantity

    def remove_product(self, product_id, quantity):
        if quantity <= 0 or self.products[product_id] is None or self.products[product_id] < quantity:
            raise Exception("wrong quantity chosen")
        else:
            self.products[product_id] -= quantity
        if self.products[product_id] == 0:
            self.products.pop(product_id)

    def get_product_list(self):
        return self.product_id_list
