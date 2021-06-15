from threading import Lock

from pony.orm import db_session

from OnlineStore.src.data_layer import user_entity
from OnlineStore.src.data_layer.receipt import Receipt


class StorePurchaseHistory:
    def __init__(self):
        self.purchases = dict()
        self.lock = Lock()

    @db_session
    def add_purchase(self, purchase: Receipt):
        self.lock.acquire()
        if purchase.receipt_id in self.purchases:
            self.lock.release()
            raise Exception(f"purchase id: {purchase.receipt_id} already exists")
        self.purchases[purchase.receipt_id] = purchase
        purchase_history = user_entity.StorePurchaseHistory(store_name=purchase.store_name,
                                                            receipt_id=purchase.receipt_id,
                                                            user_name=purchase.user_name,
                                                            total_sum=purchase.total_sum, date=purchase.date,
                                                            destination=purchase.destination,
                                                            transaction_id=purchase.transaction_id)

        for k, p in purchase.products.items():
            purchase_history.products.add(
                user_entity.ProductInHistoryStore(quantity=p, product_name=k, store_purchase_history=purchase_history))

        self.lock.release()

    def get_purchase_history(self):
        purchases = list()
        for receipt in self.purchases.values():
            purchases.append(vars(receipt))
        return purchases
