import datetime
from OnlineStore.src.dto.cart_dto import CartDTO

# the supply system rejects all the deliveries to haifa

def address_supply_system(cart: CartDTO, user_information) -> datetime.datetime:
    if user_information == "haifa":
        raise Exception("Delivery system rejected the delivery")
    else:
        return datetime.datetime.today() + datetime.timedelta(days=1)
