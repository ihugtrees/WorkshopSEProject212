from OnlineStore.src.domain_layer.store.inventory import Inventory
from OnlineStore.src.dto.product_dto import ProductDTO


class InventoryDTO:
    def __init__(self, inventory: Inventory):
        self.products_dict = dict()
        for product in inventory.products_dict.values():
            self.products_dict[product.product_id] = ProductDTO(product)
