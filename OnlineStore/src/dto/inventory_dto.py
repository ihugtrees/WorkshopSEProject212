from OnlineStore.src.domain.store.inventory import Inventory
from OnlineStore.src.dto.product_dto import ProductDTO


class InventoryDTO:
    def __init__(self, inventory: Inventory):
        self.products_dict = dict()
        for product in inventory.products_dict:
            self.products_dict[product.product_name] = ProductDTO(product)
