from datetime import datetime

from pony.orm import *

db = Database()


class User(db.Entity):
    user_name = PrimaryKey(str)
    is_guest = Required(bool)
    is_admin = Required(bool)
    age = Required(int)
    permissions = Required(int)
    productInCart = Set("ProductInCart")
    pendingMessages = Set("PendingMessages")
    historyMessages = Set("HistoryMessages")
    userPurchaseHistory = Set("UserPurchaseHistory")
    userPermissions = Set('UserPermissions')
    appoint = Set('Appoint')

class PendingMessages(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Required(User)
    message_content = Required(str)
    event = Required(str)

class HistoryMessages(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Required(User)
    message_content = Required(str)
    event = Required(str)

class ProductInCart(db.Entity):
    user = Required(User)
    store_name = Required(str)
    product = Required(str)
    quantity = Required(int)
    PrimaryKey(user, store_name, product)


class Store(db.Entity):
    name = PrimaryKey(str, auto=False)
    store_founder = Required(str)
    rating = Optional(int)
    products = Set('Product')
    buying_policy = Set('BuyingPolicy')
    discount_policy = Set('DiscountPolicy')


class Product(db.Entity):
    store = Required(Store)
    product_id = Required(str)
    product_name = Required(str)
    quantity = Required(int)
    description = Optional(str)
    price = Required(int)
    category = Required(str)
    rating = Optional(int)
    PrimaryKey(store, product_id)


class BuyingPolicy(db.Entity):
    name = PrimaryKey(str)
    description = Required(str)
    store = Required(Store)



class DiscountPolicy(db.Entity):
    name = PrimaryKey(str)
    description = Required(str)
    store = Required(Store)
    value = Required(str)
    category_flag_for_value = Optional(bool)


#
#
# class BuyingTerm(db.Entity):
#     pass
#     term_name = Required(str) TODO COMPLETE

class UserPermissions(db.Entity):
    user_name = Required(User)
    store_name = Required(str)
    store_permissions = Required(int)
    PrimaryKey(user_name, store_name)


class Appoint(db.Entity):
    user_name = Required(User)
    store_name = Required(str)
    appointee = Required(str)
    PrimaryKey(user_name, store_name, appointee)


class UserPurchaseHistory(db.Entity):
    store_name = Required(str)
    receipt_id = Required(str)
    user_name = Required(User)
    total_sum = Required(int)
    date = Required(datetime)
    destination = Required(str)
    products = Set("ProductInHistory")
    transaction_id = Required(int)
    PrimaryKey(user_name, receipt_id)


class ProductInHistory(db.Entity):
    product_name = Required(str)
    quantity = Required(int)
    user_purchase_history = Required(UserPurchaseHistory)
