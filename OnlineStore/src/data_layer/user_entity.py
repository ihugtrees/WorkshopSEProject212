from pony.orm import *

db = Database()


class User(db.Entity):
    user_name = PrimaryKey(str)
    is_guest = Required(bool)
    is_admin = Required(bool)
    appointed_to_store = Optional('Appoint')
    age = Required(int)
    productInCart = Set("ProductInCart")
    pendingMessages = Set("PendingMessages")
    historyMessages = Set("HistoryMessages")

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


class Appoint(db.Entity):
    user = Required(User)
    appointed_by_me = Set('Appointees')


class Appointees(db.Entity):
    appoint = Required(Appoint)
    store_name = Required(str)
    appointees = Optional(StrArray)


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


    # class PendingMessage(db.Entity):
    #     user_name = Required(str)
    #     msg = Required(str)
    #     event = Required(str)
    #
    #
    # class Message(db.Entity):
    #     user_name = Required(str)
    #     msg = Required(str)
    #     event = Required(str)


class UserPermissions(db.Entity):
    user_name = Required(str)
    permissions = Required(int)
    permissions_in_store = Set('PermissionsInStore')


class PermissionsInStore(db.Entity):
    user_permissions = Required(UserPermissions)
    store_name = Required(str)
    permissions = Required(int)


# class Purchase(db.Entity):
#     store = Required(str)
#     user = Required(str)
#
