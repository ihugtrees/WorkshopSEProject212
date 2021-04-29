from OnlineStore.src.domain.store.purchase import Purchase


class PurchaseDTO:
    def __init__(self, purchase: Purchase):  # change purchase history from none to empty list (yonatan)
        self.purchase_id = purchase.purchase_id
        self.user_name = purchase.user_name
        self.store_name = purchase.store_name
