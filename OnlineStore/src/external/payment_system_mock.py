# 2.9.1
# the payment system reject all card_numbers that equal to 0000
def address_payment_system(payment_details: dict, sum: int):
    if payment_details["card_number"] == "0000":
        raise Exception("Payment system rejected the card")
    else:
        return True
