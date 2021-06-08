import OnlineStore.src.domain_layer.user.user as user
from pony.orm import *
import OnlineStore.src.data_layer.user_entity as user_entity
from OnlineStore.src.domain_layer.user.basket import Basket
from OnlineStore.src.domain_layer.user.cart import Cart
from OnlineStore.src.domain_layer.user.user import User
from OnlineStore.src.dto import user_dto, cart_dto

users: dict = dict()  # key - user name, value User
pending_messages: dict = dict()  # key: username, value: list of messages
history_messages: dict = dict()



def take_user_data(user_name):
    user_db = user_entity.User.get(user_name = user_name)
    basket_db = user_entity.ProductToBuy.select(lambda p: p.user.user_name == user_name)
    stores = set()
    for p in basket_db:
        stores.add(p.store_name)
    basket_dict = dict()
    for s in stores:
        product_dict = dict()
        for p in basket_db:
            if p.store_name == s:
                product_dict[p.product] = p.quantity
        basket = Basket()
        basket.products_dict = product_dict
        basket_dict[s] = basket
    cart = Cart()
    cart.basket_dict = basket_dict
    new_user = User(user_db.user_name, cart, user_db.is_admin, user_db.appointed_to_store, age= user_db.age)
    users[user_name] = new_user
    return new_user



# def cart_db_to_domain_cart(db_cart: user_entity.Cart):
#     cart: user.Cart = user.Cart()
#     for db_basket in (db_cart.basket_dict if db_cart is not None else list()):
#         store_name = db_basket.store_name
#         for basket_item in db_basket.products_dict:
#             cart.add_product_to_cart(store_name=store_name, product_id=basket_item.product_name,
#                                      quantity=basket_item.quantity)
#     return cart


def db_appoint_to_user_appoint(appointed_to_store: user_entity.Appoint):
    domain_appoint = user.Appoint()
    for appointee in (appointed_to_store.appointed_by_me if appointed_to_store is not None else list()):
        for store_employee_name in appointee.appointees:
            domain_appoint.assign_store_employee(new_store_owner_name=store_employee_name,
                                                 store_name=appointee.store_name)
    return domain_appoint


def user_db_to_domain_user(user_db: user_entity.User):
    return user.User(user_name=user_db.user_name, is_admin=user_db.is_admin,
                     guest=user_db.is_guest, cart=cart_db_to_domain_cart(user_db.cart), age=user_db.age,
                     appointed_to_store=db_appoint_to_user_appoint(user_db.appointed_to_store))


@db_session
def get_user_by_name(user_name) -> user.User:
    if user_name in users:
        return users[user_name]
    else:
        return take_user_data(user_name)


@db_session
def add_user(usr: user.User) -> None:
    user_db = user_entity.User.get(user_name=usr.user_name)
    if user_db is not None:
        raise Exception("user already exists")
    db_user = user_entity.User(user_name=usr.user_name, is_guest=usr.is_guest,
                               is_admin=usr.is_admin, age=usr.age)


def remove_user(user_name: str) -> None:
    if user_name not in users:
        raise Exception("cannot remove: user already does not exist in the system")
    users.pop(user_name)


def pop_user_messages(username: str) -> list:
    """

    :param username:
    :return: list of messages (message = {"message": str, "event": str})
    """
    if username not in pending_messages:
        # raise Exception("User does not have messages")
        return list()
    return pending_messages.pop(username)


def add_message(username, message, event) -> None:
    if username not in pending_messages:
        pending_messages[username] = list()
    pending_messages[username].append({"message": message, "event": event})


def add_message_to_history(username, message, event) -> None:
    if username not in history_messages:
        history_messages[username] = list()
    history_messages[username].append({"message": message, "event": event})


def get_user_message_history(user_name):
    if user_name not in history_messages:
        return list()
    else:
        return history_messages[user_name]


@db_session
def add_to_cart(user_name, product_name, quantity, store_name):
    product_user = user_entity.ProductToBuy.select(lambda p: p.user == user_name and
                                        p.product == product_name and p.store_name == store_name)


    # user_db = user_entity.User.get(user_name=user_name)
    # if user_db is None:
    #     raise Exception("user does not exist")
    # user_db.cart = user_db.cart if user_db.cart is not None else user_entity.Cart(user=user_db, basket_dict=[])
    # try:
    #     new_basket = user_entity.Basket(cart=user_db.cart, store_name=store_name, products_dict=[])
    #     new_basket.products_dict.add(user_entity.BasketItem(basket=new_basket, product_name=product_name, quantity=quantity))
    # except Exception as e:
    #     new_basket = user_entity.Basket.get(cart=user_db.cart, store_name=store_name)
    #     basket_item = user_entity.BasketItem.get(basket=new_basket, product_name=product_name)
    #     if basket_item is None:
    #         new_basket.products_dict.add(user_entity.BasketItem(basket=new_basket, product_name=product_name, quantity=quantity))
    #     else:
    #         basket_item.set(quantity=(basket_item.quantity + quantity))


def remove_from_cart(user_name, product_name, quantity, store_name):
    product_user = user_entity.ProductToBuy.select(lambda p: p.user == user_name and
            p.product == product_name and p.store_name == store_name)
    # if user_db is None:
    #     raise Exception("user does not exist")
    # if user_db.cart is None:
    #     raise Exception("Cart does not exist!")
    # basket = user_entity.Basket.get(cart=user_db.cart, store_name=store_name)
    # if basket is None:
    #     raise Exception("basket does not exist!")
    # basket_item = user_entity.BasketItem(basket=basket, product_name=product_name)
    # if basket_item is None:
    #     raise Exception("Product is not in the cart")
    # if (basket_item.quantity-quantity) < 0:
    #     raise Exception("Quantity violation")
    # basket_item.set(quantity=(basket_item.quantity - quantity))
