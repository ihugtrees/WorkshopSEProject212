import random


class MockPaymentSystem:
# 2.9.1
# the payment system reject all card_numbers that equal to 0000
    def pay(self, payment_info: dict):
        if payment_info["card_number"] == "0000":
            raise Exception("Payment system rejected the card")
        else:
            return random.randint(0, 100000)

    def cancel_pay(self, transaction_id):
        if transaction_id == "1111":
            raise Exception("cancel pay fail!")
