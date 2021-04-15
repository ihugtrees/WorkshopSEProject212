class Product:
    def __init__(self, product_id, product_name: str, quantity: int):
        self.product_name = product_name
        self.quantity = quantity
        self.description = ""

    def edit_product_description(self, product_description: str):
        self.description = product_description

    def take_quantity(self, num_to_take):
        self.quantity = self.quantity - num_to_take

    def add_quantity(self, num_to_add):
        self.quantity = self.quantity + num_to_add
