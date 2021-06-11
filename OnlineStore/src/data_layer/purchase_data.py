from threading import Lock

from OnlineStore.src.data_layer.receipt import Receipt
from OnlineStore.src.domain_layer.store.store_purchase_history import StorePurchaseHistory
from OnlineStore.src.domain_layer.user.user_handler import get_random_string
from OnlineStore.src.domain_layer.user.user_purchase_history import UserPurchaseHistory
from OnlineStore.src.dto.cart_dto import CartDTO

user_purchases: dict = dict()
store_purchases: dict = dict()
purchase_lock = Lock()


def get_purchase_by_id(user_name: str, purchase_id: str) -> Receipt:
    purchase_obj: UserPurchaseHistory = user_purchases.get(user_name)
    if purchase_obj is None:
        raise Exception(f"The {user_name} does not have any purchase history logged")
    return purchase_obj.get_purchase_by_id(purchase_id)


def get_user_purchase_history(user_name: str) -> list:
    purchase_obj: UserPurchaseHistory = user_purchases.get(user_name)
    if purchase_obj is None:
        raise Exception(f"The {user_name} does not have any purchase history logged")
    return purchase_obj.get_purchase_history()


def get_store_history_purchases(store_name: str) -> list:
    purchase_obj: StorePurchaseHistory = store_purchases.get(store_name)
    if purchase_obj is None:
        raise Exception(f"{store_name} does not have any purchase history logged")
    return purchase_obj.get_purchase_history()


def add_receipt(receipt: Receipt) -> None:
    purchase_obj = user_purchases.get(receipt.user_name)
    if purchase_obj is None:
        purchase_obj = UserPurchaseHistory()
    purchase_obj.add_purchase(receipt)
    user_purchases[receipt.user_name] = purchase_obj
    purchase_obj = store_purchases.get(receipt.store_name)
    if purchase_obj is None:
        purchase_obj = StorePurchaseHistory()
    purchase_obj.add_purchase(receipt)
    store_purchases[receipt.store_name] = purchase_obj


def add_all_basket_purchases_to_history(cart: CartDTO, user_name, cart_sum, date, destination, transaction_id):
    for store_name, basket in cart.basket_dict.items():
        while True:
            try:
                receipt = Receipt(get_random_string(20), user_name, store_name, cart_sum, date, destination,
                                  basket.products_dict,transaction_id)
                add_receipt(receipt)
                break
            except:
                continue
