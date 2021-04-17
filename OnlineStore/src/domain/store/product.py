class Product:
    def __init__(self, product_id, product_name: str, quantity: int):
        self.product_name = product_name
        self.quantity = quantity
        self.description = ""
        self.discount_type = None
        self.buying_type = None
        self.price = 10  # TODO NEED TO CHANGE TO CONSTRUCTOR VARIABLE

    def edit_product_description(self, product_description: str):
        self.description = product_description

    def take_quantity(self, num_to_take):
        if self.quantity < num_to_take:
            raise Exception("There are only " + num_to_take + " from" + self.product_name + " in the store.\n")
        self.quantity = self.quantity - num_to_take

    def add_quantity(self, num_to_add):
        self.quantity = self.quantity + num_to_add

    def calculate_product_sum(self, quantity: int) -> int:
        # TODO FOR NOW ONLY QUANTITY*PRICE
        return self.price*quantity
