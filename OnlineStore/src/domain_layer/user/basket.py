class Basket:
    def __init__(self):
        self.products_dict = dict()  # key-product_id , value-quantity

    def add_product_to_basket(self, product_id, quantity):
        if quantity <= 0:
            raise Exception("wrong quantity chosen")

        if product_id not in self.products_dict:
            self.products_dict[product_id] = quantity
        else:
            self.products_dict[product_id] += quantity

    def remove_product_from_basket(self, product_id, quantity):
        if quantity <= 0 or product_id not in self.products_dict or self.products_dict[product_id] < quantity:
            raise Exception("wrong quantity chosen")
        else:
            self.products_dict[product_id] -= quantity

        if self.products_dict[product_id] == 0:
            self.products_dict.pop(product_id)

    def get_product_dict(self):
        return self.products_dict

    def get_str_basket(self):
        output = ""
        for id in self.products_dict:
            output=output+"Product id : "+id+" quantity : "+self.products_dict[id]+"\n"
