import datetime


# 8
from OnlineStore.src.dto.cart_dto import CartDTO


def address_supply_system(cart: CartDTO, user_information) -> datetime.datetime:
    return datetime.datetime.today() + datetime.timedelta(days=1)
