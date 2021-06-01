import OnlineStore.src.external.payment_system as payment_system


def pay(payment_info: dict):
    payment_system.pay(payment_info)


def cancel_pay(transaction_id: int) -> None:
    payment_system.cancel_pay(transaction_id)
