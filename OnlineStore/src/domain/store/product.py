class Product:
    def __init__(self, product_id, product_name: str, quantity: int, category: str = "null"):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.description = ""
        self.category = category

    def take_quantity(self, quant):
        if quant <= 0 or self.quantity < quant:
            raise Exception("Not enough product")
        self.quantity -= quant

    def add_quantity(self, quant):
        if quant <= 0:
            raise Exception("cant add less than one quantity")
        self.quantity += quant

    def edit_product_description(self, product_description):
        if type(product_description) != str:
            raise Exception("description must be string")
        self.description = product_description
