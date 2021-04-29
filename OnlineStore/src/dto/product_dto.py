from OnlineStore.src.domain.store.product import Product


class ProductDTO:
    def __init__(self, product: Product):
        self.product_id = product.product_id
        self.product_name = product.product_name
        self.quantity = product.quantity
        self.description = product.description
        self.discount_type = product.discount_type
        self.buying_type = product.buying_type
        self.price = product.price
        self.category = product.category
        self.rating = product.rating
