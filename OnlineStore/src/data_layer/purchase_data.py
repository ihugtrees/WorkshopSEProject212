from OnlineStore.src.domain.store.purchase import Purchase

purchases: dict = dict()


def get_purchase_by_id(purchase_id: str) -> Purchase:
    purchase = purchases.get(purchase_id)
    if purchase is None:
        raise Exception("purchase does not exist")
    return purchase


def get_user_purchases(user_name: str) -> list:
    purchase_list = list()
    for purchase in purchases.values():
        if purchase.user_name is user_name:
            purchase_list.append(purchase)
    return purchase_list


def get_store_purchases(store_name: str) -> list:
    purchase_list = list()
    for purchase in purchases.values():
        if purchase.store_name is store_name:
            purchase_list.append(purchase)
    return purchase_list


def add_purchase(purchase: Purchase) -> None:
    if purchase.purchase_id in purchases:
        raise Exception("purchase id already exists")
    purchases[purchase.purchase_id] = purchase
