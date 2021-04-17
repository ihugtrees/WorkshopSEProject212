from OnlineStore.src.domain.external.payment_system import address_payment_system
from OnlineStore.src.domain.external.supply_system import address_supply_system
from OnlineStore.src.domain.store.store import Store
from OnlineStore.src.domain.user.action import Action
from OnlineStore.src.domain.user.user_handler import UserHandler
from OnlineStore.src.domain.store.store_handler import StoreHandler
from OnlineStore.src.service.authentication import Authentication
#from OnlineStore.src.service.event import Event
#from OnlineStore.src.service.event_log import Event_Log
from OnlineStore.src.service.logger import Logger

logging = Logger()

user_handler = UserHandler()
store_handler = StoreHandler()
auth = Authentication()


# 2.1
def get_into_site() -> str:
    try:
        ans = user_handler.get_guest_unique_user_name()
        logging.info("get_into_site")
        return [True, ans]
    except Exception as e:
        logging.error("fail in get_into_site: " + e.args[0])
        return [False, e.args[0]]

# 2.2
def exit_the_site(guest_name):
    try:
        ans = user_handler.exit_the_site(guest_name)
        logging.info("exit_the_site")
        return [True, ans]
    except Exception as e:
        logging.error("fail in exit_the_site: " + e.args[0])
        return [False, e.args[0]]


# 2.3
def register(user_name, password):
    try:
        if auth.register(user_name, password):
            ans = user_handler.register(user_name)
            logging.info("register")
            return [True, ans]
        else:
            logging.info("register: user already exist")
            return [False, Exception("user already exist")]
    except Exception as e:
        logging.error("faili in register: " + e.args[0])
        return [False, e.args[0]]


# 2.4
def login(user_name, password):
    try:
        if auth.login(user_name, password):
            ans = user_handler.login(user_name)
            logging.info("login " + user_name + ", " + password)
            return [True, ans]
        else:
            logging.info("login: invalid input")
            return [False, Exception("login fail")]
    except Exception as e:
        logging.error("fail in login: " + e.args[0])
        return [False, e.args[0]]


# 2.5.0
def get_information_about_products(store_name):
    try:
        ans = store_handler.get_information_about_products(store_name)
        logging.info("get_information_about_products " + store_name)
        return [True, ans]
    except Exception as e:
        logging.error("fail: get_information_about_products " + e.args[0])
        return [False, e.args[0]]


# 2.5.1
def get_store_info(store_name):
    try:
        ans = store_handler.get_store_info(store_name)
        logging.info("get_store_info " + store_name)
        return [True, ans]
    except Exception as e:
        logging.error("fail in get_store_info " + e.args[0])
        return [False, e.args[0]]


def get_store(store_name):
    try:
        ans = store_handler.get_store(store_name)
        logging.info("get store " + store_name)
        return [True, ans]
    except Exception as e:
        logging.error("get_store faild " + e.args[0])
        return [False, e.args[0]]


def add_product_to_store(user_name, product_details, store_name):
    try:
        ans = store_handler.add_new_product_to_store_inventory(user_name, product_details, store_name)
        logging.info("add_product_to_store " + user_name + store_name)
        return [True, ans]
    except Exception as e:
        logging.error("add_product_to_store faild, " + e.args[0])
        return [False, e.args[0]]


# # 2.6
# def find_products(p_name, category, key_word, filter_options):
#     pass

# 2.6
def search_product_by_id(product_id):
    try:
        for store in store_handler.store_dict:
            if product_id in store_handler.store_dict[store].inventory.products_dict:
                ans = store_handler.store_dict[store].inventory.products_dict[product_id]
                logging.info("search_product_by_id" + product_id)
                return [True, ans]
        logging.info("search_product_by_id " + "product not found")
        return [False, "product not found"]
    except Exception as e:
        logging.error("search_product_by_id fail " + e.args[0])
        return [False, "bug, when searching by name"]


"""
filters = 
{
min: int
max: int
prating: int
category: str
srating: int
}
"""


def get_stores_with_rating(rating):
    if rating is None:
        rating = 0
    store_list = list()
    for key, store in store_handler.store_dict.items():
        if store.rating >= rating:
            store_list.append(store)
    return store_list


def get_products_with_filters(store, filters):
    min_price = 0
    rating = 0
    cat = ''

    if filters['min'] is not None:
        min_price = filters['min']
    if filters['prating'] is not None:
        rating = filters['prating']
    if filters['category'] is not None:
        cat = filters['category']

    product_list = list()
    if filters['max'] is not None:
        for key, product in store_handler.store_dict[store].inventory.products_dict.items():
            if min_price <= product.price <= filters['max'] and rating <= product.rating and product.category.find(
                    cat) != -1:
                product_list.append(product)
    else:
        for key, product in store_handler.store_dict[store].inventory.products_dict.items():
            if min_price <= product.price and rating <= product.rating and product.category.find(cat) != -1:
                product_list.append(product)
    return product_list


# 2.6.1
def search_product_by_category(category, filters):
    try:
        if filters['category'] is not None and category.find(filters['category']) == -1:
            return [False, "category doesnt match"]
        product_list = list()
        for store in get_stores_with_rating(filters['srating']):
            for product in get_products_with_filters(store.name, filters):
                if product.category.find(category) != -1:
                    product_list.append(product)
        if len(product_list) == 0:
            logging.info("search_product_by_category: category: "+ category+ "product not found")
            return [False, "product not found"]
        else:
            logging.info("search_product_by_category: category: " + category)
            return [True, product_list]
    except Exception as e:
        logging.error("search_product_by_category fail: " + e.args[0])
        return [False, "bug, when searching by category"]


def find_product_by_id(product_id, store_name):  # TODO
    try:
        ans = store_handler.find_product_by_id(product_id, store_name)
        logging.info("find_product_by_id: id = " + product_id + "store name = " + store_name)
        return [True, ans]
    except Exception as e:
        logging.error("find_product_by_id FAIL:  + id = " + product_id + "store name = " + store_name)
        return [False, e.args[0]]


# 2.6.3
def find_product_by_keyword(keyword, filters):
    try:
        product_list = list()
        for store in get_stores_with_rating(filters['srating']):
            for product in get_products_with_filters(store, filters):
                if product.description.find(keyword) != -1:
                    product_list.append(product)
        if len(product_list) == 0:
            return [False, "product not found"]
        else:
            return [True, product_list]
    except Exception as e:
        return [False, "bug, when searching by keyword"]


# 2.6.4
# def filter_product_by_price(product_list):
#     try:
#         for product in product_list:
#
#         if len(product_list) == 0:
#             return [False, "product not found"]
#         else:
#             return [True, product_list]
#     except Exception as e:
#         return [False, "bug, when searching by keyword"]


# 2.7
def save_cart(user_name):
    pass


# 2.8.1
def get_cart_info(user_name):
    try:
        ans = user_handler.get_cart_info(user_name)
        logging.info("get_cart_info: user name = " + get_cart_info)
        return [True, ans]
    except Exception as e:
        logging.error("get_cart_info fail user name = "+ user_name + e.args[0])
        return [False, e.args[0]]


def get_cart(user_name):
    try:
        ans = user_handler.get_cart(user_name)
        logging.info("get_cart")
        return [True, ans]
    except Exception as e:
        logging.error("get_cart fail " + e.args[0])
        return [False, e.args[0]]


"""EDIT THE CART FUNCTIONS"""


# 2.8.2
def add_product_to_cart(user_name, product_id, quantity, store_name):
    try:
        store_handler.check_product_exists_in_store(product_id, store_name)
        ans = user_handler.add_product(user_name, store_name, product_id, quantity)
        logging.info("add_product_to_cart")
        return [True, ans]
    except Exception as e:
        logging.error("add_product_to_cart fail: " + e.args[0])
        return [False, e.args[0]]


# 2.8.3
def remove_product(user_name, product_id, quantity, store_name):
    try:
        ans = user_handler.remove_product(user_name, product_id, quantity, store_name)
        logging.info("remove_product")
        return [True, ans]
    except Exception as e:
        logging.error("remove_product fail: " + e.args[0])
        return [False, e.args[0]]


# 2.9.0
def purchase(user_name: str, payment_info: dict, destination: str):
    """
    Purchase all the items in the cart

    :param destination: the address of the customer
    :param user_name: user name
    :param payment_info: {credit_num: str, three_digits: str, expiration_date: date}
    :return: [boolean, T] -> if boolean is false T is a string representation of the problem if boolean is true T is expected time of delivery
    """
    try:
        user = get_user(user_name)[1]
        cart = user.cart
        store_handler.is_valid_for_purchase(cart, user)
        store_handler.take_quantity(cart)
        cart_sum = store_handler.calculate_cart_sum(cart)
        address_payment_system(payment_info, cart_sum)
        date = address_supply_system(cart, destination)
        user.empty_cart()
        logging.info("purchase user name = " + user)
        return [True, date]
    except Exception as e:
        logging.error("purchase fail " + e.args[0])
        return [False, e.args[0]]


# 3.1
def logout(user_name):
    try:
        ans = user_handler.logout(user_name)
        logging.info("logout user name: " + user_name)
        return [True, ans]
    except Exception as e:
        logging.error("logout fail " + e.args[0])
        return [False, e.args[0]]


# 3.2, think about arguments and preconditions
def open_store(store_name, user_name):
    try:
        user_handler.check_permission_to_open_store(user_name)
        ans = store_handler.open_store(store_name, user_name)
        logging.info("open_store user name: " + user_name + " store name: "+ store_name)
        return [True, ans]
    except Exception as e:
        logging.error("open_store fail: " + e.args[0])
        return [False, e.args[0]]


# 3.7
def get_user_purchases_history(user_name):
    try:
        ans = user_handler.get_user_purchase_history(user_name)
        logging.info("get_user_purchases_history: user name: " + user_name)
        return [True, ans]
    except Exception as e:
        logging.error("get_user_purchases_history fail: " + e.args[0])
        return [False, e.args[0]]


# 4.1.1
def add_new_product_to_store_inventory(user_name, product_details, store_name):
    """

    :param user_name:
    :param product_details: (dict)
    :param store_name:
    :return:
    """
    try:
        ans = store_handler.add_new_product_to_store_inventory(user_name, product_details, store_name)
        logging.info("add_new_product_to_store_inventory: store name: " + store_name)
        return [True, ans]
    except Exception as e:
        logging.error("add_new_product_to_store_inventory fail: " + e.args[0])
        return [False, e.args[0]]


# 4.1.2
def remove_product_from_store_inventory(user_name, product_id, store_name):
    """
    removes a @product_id from a store named @store_name

    :param user_name: user name of whom who asked to remove the product
    :param product_id: product id to remove
    :param store_name: store name to remove from
    :return: [boolean, T] -> if boolean is false T is a string representation of the problem
    if boolean is true T is None
    """
    try:
        ans = store_handler.remove_product_from_store_inventory(user_name, product_id, store_name)
        logging.info("remove_product_from_store_inventory: product ID: " + product_id)
        return [True, ans ]
    except Exception as e:
        logging.error("remove_product_from_store_inventory fail: " +e.args[0])
        return [False, e.args[0]]


# 4.1.3
def edit_product_details(user_name, product_details, store_id, product_id):
    try:
        store_handler.store_dict[store_id].check_permission_to_edit_store_inventory(user_name)
        ans = store_handler.store_dict[store_id].edit_product(product_id, product_details)
        logging.info("edit_product_details")
        return [True, ans]
    except Exception as e:
        logging.error("edit_product_details fail: " + e.args[0])
        return [False, e.args[0]]


# 4.3
def assign_store_owner(user_name, new_store_owner_id, store_id):
    try:
        store: Store = store_handler.store_dict[store_id]
        if store.check_permission_to_assign(user_name):
            ans = store.assign_new_owner(new_store_owner_id, user_name)
            logging.info("assign_store_owner")
            return True, ans
        else:
            logging.info("assign_store_owner: " + user_name + " is not owner of " + store_id)
            return False, (user_name + " is not owner of " + store_id)
    except Exception as e:
        logging.error("assign_store_owner fail: " + e.args[0])
        return False, (user_name + " is not owner of " + store_id)


# 4.5
def assign_store_manager(user_name, new_store_manager_id, store_id):
    try:
        store: Store = store_handler.store_dict[store_id]
        if store.check_permission_to_assign(user_name):
            ans = store.assign_new_manager(new_store_manager_id, user_name)
            user_handler.users_dict[new_store_manager_id].set_permissions(1, store_id)
            logging.info("assign_store_manager")
            return True, ans
        else:
            logging.info("assign_store_manager " + user_name + " is not owner of " + store_id)
            return False, (user_name + " is not owner of " + store_id)
    except Exception as e:
        logging.error("assign_store_manager "+ e.args[0])
        return False, (user_name + " is not owner of " + store_id)


# 4.6
def edit_store_manager_permissions(user_name: str, store_manager_name: str, new_permissions: int, store_name: str):
    try:
        store_handler.is_manager_assigner(user_name, store_name, store_manager_name)
        ans = user_handler.edit_store_manager_permissions(user_name, store_manager_name, new_permissions)
        logging.info("edit_store_manager_permissions")
        return [True, ans]
    except Exception as e:
        logging.error("edit_store_manager_permissions " + e.args[0])
        return [False, e.args[0]]


# 4.7
def remove_store_manager(user_name, store_manager_id, store_id):
    try:
        store: Store = store_handler.store_dict[store_id]
        ans = store.delete_manager(store_manager_id, user_name)
        logging.info("remove_store_manager")
        return True, ans
    except Exception as e:
        logging.error("remove_store_manager " + e.args[0])
        return False, e.args[0]


# 4.9.1
def get_employee_information(user_name: str, employee_name: str, store_name: str):
    try:
        user_handler.is_permitted_to_do(user_name, store_name, 1 << Action.EMPLOYEE_INFO.value)
        ans = user_handler.get_employee_information(employee_name)
        logging.info("get_employee_information")
        return [True, ans]
    except Exception as e:
        logging.error("get_employee_information " + e.args[0])
        return [False, e.args[0]]


# 4.9.1
# def get_employee_information(user_name, employee_id):
#     pass


# 4.9.2
def get_employee_permissions(user_name: str, store_name: str, employee_name: str):
    try:
        user_handler.is_permitted_to_do(user_name, store_name, 1 << Action.EMPLOYEE_PERMISSIONS.value)
        return [True, user_handler.get_employee_information(
            employee_name)]  # TODO FOR NOW RETURN INFORMATION MAYBE TO CHANGE TO NEW FUNCTION
    except Exception as e:
        return [False, e.args[0]]


# 4.11
def get_store_purchase_history(user_name, store_name):
    try:
        user_handler.is_permitted_to_do(user_name, store_name, 1 << Action.STORE_PURCHASE_HISTORY.value)
        return [True, store_handler.get_store_purchase_history(store_name)]
    except Exception as e:
        return [False, e.args[0]]


# 6.4.1
def get_store_purchase_history_admin(user_name, store_name):
    get_store_purchase_history(user_name, store_name)


# 6.4.2
def get_user_purchase_history_admin(user_name, other_user_name):
    try:
        user_handler.is_permitted_to_do(user_name, None, 1 << Action.USER_PURCHASE_HISTORY.value)
        return [True, user_handler.get_user_purchase_history(other_user_name)]
    except Exception as e:
        return [False, e.args[0]]


def get_store(store_id):
    try:
        store = store_handler.store_dict[store_id]
        return True, store
    except Exception as e:
        return False, e.args[0]


def get_user(user_name):
    try:
        user = user_handler.users_dict[user_name]
        return [True, user]
    except Exception as e:
        return [False, e.args[0]]
