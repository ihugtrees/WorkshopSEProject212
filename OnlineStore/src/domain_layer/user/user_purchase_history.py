from OnlineStore.src.data_layer.receipt import Receipt
from threading import Lock

class UserPurchaseHistory:
    def __init__(self):
        self.purchases = dict()
        self.lock = Lock()

    def add_purchase(self, purchase: Receipt):
        self.lock.acquire()
        if purchase.receipt_id in self.purchases:
            self.lock.release()
            raise Exception(f"purchase id: {purchase.receipt_id} already exists")
        self.purchases[purchase.receipt_id] = purchase
        self.lock.release()

    def get_purchase_history(self):
        return self.purchases.values()

    def get_purchase_by_id(self, purchase_id: str):
        purchase = self.purchases.get(purchase_id)
        if purchase is None:
            raise Exception(f"Purchase: {purchase_id} does not exist!")
        return purchase
