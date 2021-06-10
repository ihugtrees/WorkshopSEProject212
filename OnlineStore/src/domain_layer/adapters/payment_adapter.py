import OnlineStore.src.external.payment_system as payment_system


class PaymentAdapter:
    def __init__(self, payment_system):
        self.payment_system = payment_system

    def pay(self, payment_info: dict):
        self.payment_system.pay(payment_info)

    def cancel_pay(self, transaction_id: int) -> None:
        self.payment_system.cancel_pay(transaction_id)
