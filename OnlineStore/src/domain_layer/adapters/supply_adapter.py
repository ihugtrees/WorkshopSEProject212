import OnlineStore.src.external.supply_system_mock as supply_system
from OnlineStore.src.dto.cart_dto import CartDTO


def supply_products_to_user(cart: CartDTO, des: str):
    return supply_system.address_supply_system(cart, des)
