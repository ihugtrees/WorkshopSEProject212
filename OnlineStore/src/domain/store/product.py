class Product:
    def __init__(self, product_id, product_name: str, quantity: int):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.description = ""

    def take_quantity(self, quant):
        if quant < 0 or self.quantity < quant:
            raise Exception("Not enough product")
        self.quantity -= quant

    def add_quantity(self, quant):
        if quant < 0:
            raise Exception("cant add less than one quantity")
        self.quantity += quant

    def edit_product_description(self, product_description):
        self.description = product_description
