from pony.orm import db_session

from OnlineStore.src.data_layer import user_entity
from OnlineStore.src.domain_layer.store.buying_policy.buying_policy import BuyingPolicy
from OnlineStore.src.domain_layer.store.buying_policy.create_buying_term import CreateBuyingTerm
from OnlineStore.src.domain_layer.store.discont_policy.discount_policy import DiscountPolicy
from OnlineStore.src.domain_layer.store.discont_policy.term_discount import TermDiscount
from OnlineStore.src.domain_layer.store.inventory import Inventory
from OnlineStore.src.domain_layer.store.product import Product
from OnlineStore.src.domain_layer.store.store import Store
from threading import Lock


store_dict = dict()  # key-store name, value-store
lock = Lock()

@db_session
def store_data_form_db(store_name):
    store_db = user_entity.Store.get(name=store_name)
    products = user_entity.Product.select(lambda p: p.store.name == store_name)
    product_dict = dict()
    for p in products:
        product = Product(p.product_id, p.product_name, p.quantity, p.price, p.category)
        product_dict[p.product_name] = product
    inventory = Inventory(product_dict)
    store = Store(store_name, store_db.store_founder)
    store.inventory = inventory
    store.rating = store_db.rating
    store_dict[store_name] = store
    store.buying_policy = BuyingPolicy()
    store.buying_policy.terms_dict = get_all_buying_policy_data(store_name)
    store.discount_policy = DiscountPolicy()
    store.discount_policy.discount_dict = get_all_discount_policy_data(store_name)
    return store

@db_session
def get_all_buying_policy_data(store):
    try:
        policies = user_entity.BuyingPolicy.select(lambda p: p.store.name == store)
        policies_dict = dict()
        for p in policies:
            c: CreateBuyingTerm = CreateBuyingTerm(p.description)
            policies_dict[p.name] = (c.term, p.description)
    except Exception as e:
        return dict()
    return policies_dict

@db_session
def get_all_discount_policy_data(store):
    try:
        discounts = user_entity.DiscountPolicy.select(lambda d: d.store.name == store)
        discounts_dict = dict()
        for d in discounts:
            t = TermDiscount(term_string=d.description, discount_description_products=d.value,
                                            discount_description_categories=d.category_flag_for_value)
            if t.term == None:
                discounts_dict[d.name] = (t, "term: " + "None" + ", value: " + d.value)
            else:
                discounts_dict[d.name] = (t, "term: " + d.description + ", value: " + d.value)
    except Exception as e:
        return dict()
    return discounts_dict





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
def add_product_to_store(store_name,product_details):
    user_entity.Product(store=store_name,
    product_id = product_details["product_id"],
    product_name = product_details["product_name"],
    quantity = product_details["quantity"],
    description = "harta brata",
    price = product_details["price"],
    category = "hrata barta",
    rating = 0 ) # maybe not?


@db_session
def remove_product_from_store(store_name, product_id):
    user_entity.Product[store_name, product_id].delete()

def get_all_stores() -> dict:
    return store_dict

@db_session
def add_discount_policy(store, name, description, value, category_flag=False):
    user_entity.DiscountPolicy(store=store, name=name, description=description, value=value, category_flag_for_value= category_flag)

@db_session
def add_buying_policy(store, name, description):
    user_entity.BuyingPolicy(store=store, name=name, description=description)
