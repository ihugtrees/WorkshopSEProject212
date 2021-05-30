from OnlineStore.src.domain_layer.store.receipt import Receipt


class PurchaseHistory:
    def __init__(self):
        self.purchases = dict()

    def add_purchase(self, purchase: Receipt):
        if purchase.receipt_id in self.purchases:
            raise Exception("purchase id already exists")
        self.purchases[purchase.receipt_id] = purchase

    def get_purchase_history(self):
        history = list()
        for pid, receipt in self.purchases.items():
            history.append(vars(receipt))
        return history
