from OnlineStore.src.domain.store.purchase import Purchase
from OnlineStore.src.dto.cart_dto import CartDTO
from OnlineStore.src.service.service import get_random_string
from threading import Lock

purchases: dict = dict()
purchase_lock = Lock()


def get_purchase_by_id(purchase_id: str) -> Purchase:
    purchase = purchases.get(purchase_id)
    if purchase is None:
        raise Exception("purchase does not exist")
    return purchase


def get_user_purchases(user_name: str) -> list:
    purchase_list = list()
    for purchase in purchases.values():
        if purchase.user_name == user_name:
            purchase_list.append(purchase)
    return purchase_list


def get_store_purchases(store_name: str) -> list:
    purchase_list = list()
    for purchase in purchases.values():
        if purchase.store_name == store_name:
            purchase_list.append(purchase)
    return purchase_list


def add_purchase(purchase: Purchase) -> None:
    purchase_lock.acquire()
    if purchase.purchase_id in purchases:
        purchase_lock.release()
        raise Exception("purchase id already exists")
    purchases[purchase.purchase_id] = purchase
    purchase_lock.release()



def add_all_basket_purchases_to_history(cart: CartDTO, user_name):
    for store_name in cart.basket_dict.keys():
        while True:
            try:
                add_purchase(Purchase(get_random_string(20), user_name, store_name))
                break
            except:
                continue
