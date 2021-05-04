from OnlineStore.src.domain.store.store import Store
from OnlineStore.src.dto.inventory_dto import InventoryDTO


class StoreDTO:
    def __init__(self, store: Store):  # change purchase history from none to empty list (yonatan)
        self.name = store.name
        self.store_founder = store.store_founder
        self.inventory = InventoryDTO(store.inventory)
        self.buying_policy = store.buying_policy
        self.discount_policy = store.discount_policy
        self.rating = store.rating
