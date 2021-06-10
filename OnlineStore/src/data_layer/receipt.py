class Receipt:
    def __init__(self, receipt_id, user_name, store_name, total_sum, date, destination, products, transaction_id=None):
        self.receipt_id = receipt_id
        self.user_name = user_name
        self.store_name = store_name
        self.total_sum = total_sum
        self.date = date
        self.destination = destination
        self.products = products
        self.transaction_id = transaction_id
