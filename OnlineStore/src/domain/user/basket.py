class Basket:
    def __init__(self):
        self.product_id_list = list()

    def add_product(self, product_id):
        self.product_id_list.append(product_id)

    def remove_product(self, product_id: int):
        self.product_id_list.remove(product_id)
        return len(self.product_id_list)

    def get_product_list(self):
        return self.product_id_list
