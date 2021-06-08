from pony.orm import db_session

from OnlineStore.src.data_layer import user_entity
from OnlineStore.src.domain_layer.store.inventory import Inventory
from OnlineStore.src.domain_layer.store.product import Product
from OnlineStore.src.domain_layer.store.store import Store
from threading import Lock


store_dict = dict()  # key-store name, value-store
lock = Lock()

@db_session
def store_data_form_db(store_name):
    store_db = user_entity.Store[store_name]
    products = user_entity.Product.select(lambda p: p.store == store_name)
    product_dict = dict()
    for p in products:
        product = Product(p.product_id, p.product_name, p.quantity, p.price, p.category)
        product_dict[products.product_name] = product
    inventory = Inventory(product_dict)
    store = Store(store_name, store_db.store_founder)
    store.inventory = inventory
    store.rating = store_db.rating
    store_dict[store_name] = store
    return store



def get_store_by_name(store_name: str) -> Store:
    lock.acquire()
    if store_name in store_dict:
        ans = store_dict[store_name]
    else:
        ans = store_data_form_db(store_name)
    lock.release()
    return ans

@db_session
def add_store(new_store: Store) -> None:
    global store_dict
    store: Store = store_dict.get(new_store.name)
    if store is not None:
        raise Exception(f"The store {new_store.name} already exist in the system!")
    store_dict[new_store.name] = new_store
    user_entity.Store(name= new_store.name, store_founder= new_store.store_founder, rating = new_store.rating)

@db_session
def add_product_to_store(store_name, product_dict):
    user_entity.Product(store = store_name,
    product_id = product_dict["product_id"],
    product_name = product_dict["product_name"],
    quantity = product_dict["quantity"],
    description = product_dict["description"],
    price = product_dict["price"],
    category = product_dict["category"],
    rating = 0 ) # maybe not?

def remove_product_from_store(store_name, product_id):
    user_entity.Product[store_name, product_id].delete()

def get_all_stores() -> dict:
    return store_dict
