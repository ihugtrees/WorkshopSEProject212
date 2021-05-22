from OnlineStore.src.domain_layer.store.receipt import Receipt


class ReceiptDTO:
    def __init__(self, receipt: Receipt):  # change purchase history from none to empty list (yonatan)
        self.purchase_id = receipt.receipt_id
        self.user_name = receipt.user_name
        self.store_name = receipt.store_name
