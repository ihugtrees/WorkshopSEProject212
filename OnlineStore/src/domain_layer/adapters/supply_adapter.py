from OnlineStore.src.dto.cart_dto import CartDTO
import OnlineStore.src.external.supply_system as supply_system


def supply(buyer_information: dict):
    return supply_system.supply(buyer_information)

