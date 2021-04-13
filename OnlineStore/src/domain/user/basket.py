class Basket:
    def __init__(self):
        self.products = dict()  # key-product_id , value-quantity

    def add_product_to_basket(self, product_id, quantity):
        if quantity <= 0:
            raise Exception("wrong quantity chosen")

        if product_id not in self.products:
            self.products[product_id] = quantity
        else:
            self.products[product_id] += quantity

    def remove_product_from_basket(self, product_id, quantity):
        if quantity <= 0 or product_id not in self.products or self.products[product_id] < quantity:
            raise Exception("wrong quantity chosen")
        else:
            self.products[product_id] -= quantity

        # if self.products[product_id] == 0:
        #     self.products.pop(product_id)

    def get_product_dict(self):
        return self.products
