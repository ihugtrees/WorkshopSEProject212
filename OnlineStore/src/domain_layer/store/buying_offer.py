

class BuyingOffer:
    def __init__(self, product_name: str, minimum):
        self.product_name = product_name
        self.offers = dict()   # key user_name val (quantity, price)
        self.payment_detial = dict()
        self.buyer_information = dict()
        self.minimum = int(minimum)
        self.all_acceptance = dict()  # username, owners
