from OnlineStore.src.data_layer.receipt import Receipt
from threading import Lock
from pony.orm import *
import OnlineStore.src.data_layer.user_entity as user_entity

class UserPurchaseHistory:
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
        purchase_history = user_entity.UserPurchaseHistory(store_name=purchase.store_name, receipt_id = purchase.receipt_id,
                                        user_name= purchase.user_name,total_sum = purchase.total_sum,date = purchase.date,
                                        destination= purchase.destination,transaction_id=purchase.transaction_id)
        products_list = list()

        for k,p in purchase.products.items():
            print(k)
            print(p)
            purchase_history.products.add(user_entity.ProductInHistory(quantity = p , product_name=k, user_purchase_history=purchase_history))

        self.lock.release()

    def get_purchase_history(self):
        purchases = list()
        for receipt in self.purchases.values():
            purchases.append(vars(receipt))
        return purchases

    def get_purchase_by_id(self, purchase_id: str):
        purchase = self.purchases.get(purchase_id)
        if purchase is None:
            raise Exception(f"Purchase: {purchase_id} does not exist!")
        return purchase
