from OnlineStore.src.dto.cart_dto import CartDTO
import OnlineStore.src.external.supply_system as supply_system

def supply_products_to_user(cart: CartDTO, des: str):
    return supply_system.address_supply_system(cart, des)