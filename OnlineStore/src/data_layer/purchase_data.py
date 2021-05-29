from threading import Lock

from OnlineStore.src.domain_layer.store.receipt import Receipt
from OnlineStore.src.domain_layer.user.user_handler import get_random_string
from OnlineStore.src.dto.cart_dto import CartDTO

purchases: dict = dict()
purchase_lock = Lock()


def get_purchase_by_id(purchase_id: str) -> Receipt:
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


def add_purchase(purchase: Receipt) -> None:
    purchase_lock.acquire()
    if purchase.receipt_id in purchases:
        purchase_lock.release()
        raise Exception("purchase id already exists")
    purchases[purchase.receipt_id] = purchase
    purchase_lock.release()


def add_all_basket_purchases_to_history(cart: CartDTO, user_name):
    for store_name, basket in cart.basket_dict.items():
        while True:
            try:
                receipt = Receipt(get_random_string(20), user_name, store_name, basket.products_dict)
                add_purchase(receipt)
                return receipt
            except:
                continue
