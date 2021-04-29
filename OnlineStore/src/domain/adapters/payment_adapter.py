import OnlineStore.src.external.payment_system_mock as payment_system


def pay_for_cart(payment_info: dict, sum: int):
    return payment_system.address_payment_system(payment_info, sum)
