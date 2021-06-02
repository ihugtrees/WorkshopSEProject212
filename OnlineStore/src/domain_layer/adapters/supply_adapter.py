
class SupplyAdapter:

    def __init__(self, supply_system):
        self.supply_system = supply_system

    def supply(self, buyer_information: dict):
        return self.supply_system.supply(buyer_information)

    def cancel_supply(self, transaction_id):
        return self.supply_system.supply(transaction_id)