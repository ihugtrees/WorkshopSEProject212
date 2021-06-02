import datetime

from OnlineStore.src.dto.cart_dto import CartDTO
import random


class MockSupplySystem:
    # the supply system rejects all the deliveries to haifa

    def supply(self, buyer_info: dict) -> str:
        if buyer_info["city"] == "Haifa":
            raise Exception("Delivery system rejected the delivery")
        else:
            return random.randint(0, 100000)

    def cancel_supply(self, transaction_id):
        if transaction_id == 1111:
            raise Exception("cancel supply failed")
    # print(address_supply_system(None, 'lol'))
