from OnlineStore.src.domain.store.store_handler import *
from OnlineStore.src.domain.user.guest import Guest
from OnlineStore.src.domain.user.registered import Registered
from OnlineStore.src.domain.user.user_handler import *


def main():
    #user_handler = UserHandler()
    #store_handler = StoreHandler()

    cart = Cart()
    cart.add_product_to_Cart(1, 2)
    user = Guest(cart)
    user.add_product_to_cart(20, 15)


    print("start")

main()