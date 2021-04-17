class Product:
    def __init__(self, product_id, product_name: str, quantity: int, category: str = "null"):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.description = ""
        self.discount_type = None
        self.buying_type = None
        self.price = 10  # TODO NEED TO CHANGE TO CONSTRUCTOR VARIABLE
        self.category = category

    def take_quantity(self, num_to_take):
        if self.quantity < num_to_take:
            raise Exception("There are only " + str(self.quantity) + " from " + self.product_name + " in the store.\n")
        self.quantity = self.quantity - num_to_take

    def calculate_product_sum(self, quantity: int) -> int:
        # TODO FOR NOW ONLY QUANTITY*PRICE
        return self.price*quantity

    def add_quantity(self, quant):
        if quant <= 0:
            raise Exception("cant add less than one quantity")
        self.quantity += quant

    def edit_product_description(self, product_description):
        if type(product_description) != str:
            raise Exception("description must be string")
        self.description = product_description
