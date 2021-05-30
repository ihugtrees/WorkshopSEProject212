from threading import Lock

from OnlineStore.src.data_layer.receipt import Receipt


class StorePurchaseHistory:
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
        purchases = list()
        for receipt in self.purchases.values():
            purchases.append(vars(receipt))
        return purchases
