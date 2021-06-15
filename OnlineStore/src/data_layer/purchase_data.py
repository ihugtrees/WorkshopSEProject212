from threading import Lock

from pony.orm import db_session

from OnlineStore.src.data_layer import user_entity
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


@db_session
def get_user_purchase_history(user_name: str) -> list:
    user_db = user_entity.User.get(user_name=user_name)
    if user_db is None:
        raise Exception("Store Does not exist!")
    purchases = user_db.userPurchaseHistory
    purchases_dict = dict()
    for purchase in purchases:
        products = dict()
        for product in purchase.products:
            products[product.product_name] = product.quantity
        purchases_dict[purchase.receipt_id] = Receipt(receipt_id=purchase.receipt_id, store_name=purchase.store_name,
                                                      user_name=purchase.user_name, total_sum=purchase.total_sum,
                                                      date=purchase.date, destination=purchase.destination,
                                                      transaction_id=purchase.transaction_id, products=products)
    if len(purchases_dict)==0:
        raise Exception("There is no purchase history!")
    return to_dict_tra(purchases_dict)


def to_dict_tra(purchases_dict):
    purchases = list()
    for receipt in purchases_dict.values():
        purchases.append(vars(receipt))
    return purchases


@db_session
def get_store_history_purchases(store_name: str) -> list:
    store_db = user_entity.Store.get(name=store_name)
    if store_db is None:
        raise Exception("Store Does not exist!")
    purchases = store_db.store_purchase_history
    purchases_dict = dict()
    for purchase in purchases:
        products = dict()
        for product in purchase.products:
            products[product.product_name] = product.quantity
        purchases_dict[purchase.receipt_id] = Receipt(receipt_id=purchase.receipt_id, store_name=purchase.store_name,
                                                      user_name=purchase.user_name, total_sum=purchase.total_sum,
                                                      date=purchase.date, destination=purchase.destination,
                                                      transaction_id=purchase.transaction_id, products=products)
    if len(purchases_dict)==0:
        raise Exception("There is no purchase history!")
    return to_dict_tra(purchases_dict)

    # purchase_obj: StorePurchaseHistory = store_purchases.get(store_name)
    #
    # if purchase_obj is None:
    #     raise Exception(f"{store_name} does not have any purchase history logged")
    # return purchase_obj.get_purchase_history()


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
            except Exception as e:
                continue
