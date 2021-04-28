
# 2.9.1
def address_payment_system(payment_details: dict, sum: int, success: bool):
    if success:
        return True
    else:
        raise Exception("Payment system rejected the card")
