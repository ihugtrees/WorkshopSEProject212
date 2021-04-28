import datetime
from OnlineStore.src.dto.cart_dto import CartDTO


def address_supply_system(cart: CartDTO, user_information, success: bool) -> datetime.datetime:
    if success:
        return datetime.datetime.today() + datetime.timedelta(days=1)
    else:
        raise Exception("Delivery system rejected the delivery")
