from threading import Lock


class Product:
    def __init__(self, product_id, product_name, quantity, price, category="null", discount_type=None,
                 buying_type=None):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.description = ""
        self.discount_type = discount_type
        self.buying_type = buying_type
        self.price = price
        self.category = category
        self.rating = 0
        self.lock = Lock()

    def take_quantity(self, num_to_take):
        if num_to_take <= 0 or self.quantity < num_to_take:
            raise Exception("There are only " + str(self.quantity) + " from " + self.product_name + " in the store.\n")
        self.quantity -= num_to_take

    def return_quantity(self, num_to_take):
        if num_to_take <= 0:
            raise Exception("impossible to return negative amount")
        self.lock.acquire()
        self.quantity += num_to_take
        self.lock.release()

    def calculate_product_sum(self, quantity: int) -> int:
        # TODO FOR NOW ONLY QUANTITY*PRICE
        return self.price * quantity

    def add_quantity(self, quant):
        if quant <= 0:
            raise Exception("cant add less than one quantity")
        self.quantity += quant

    def edit_product_description(self, product_description):
        if type(product_description) != str:
            raise Exception("description must be string")
        self.description = product_description
