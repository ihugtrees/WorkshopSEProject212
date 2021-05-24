import OnlineStore.src.domain_layer.domain_handler as domain_handler
from OnlineStore.src.service_layer.logger import Logger

logging = Logger()


def get_into_site():
    try:
        logging.info("get_into_site")
        return [True, domain_handler.get_into_site()]
    except Exception as e:
        logging.error("fail in get_into_site: " + e.args[0])
        return [False, e.args[0]]


def exit_the_site(guest_name):
    try:
        logging.info("exit_the_site")
        return [True, domain_handler.exit_the_site(guest_name)]
    except Exception as e:
        logging.error("fail in exit_the_site: " + e.args[0])
        return [False, e.args[0]]


def register(user_name: str, password: str, age):
    try:
        logging.info("register" + user_name)
        domain_handler.register(user_name, password, age)
        return [True, "New user has been added successfully"]
    except Exception as e:
        logging.error("fail in register: " + e.args[0])
        return [False, e.args[0]]


# 2.4
def login(user_name: str, password: str):
    """
    Login registered user to the system

    :param user_name: user name
    :param password: password
    :return: hashed user name (function as a session key)
    """
    try:
        logging.info("login " + user_name)
        user_name_hash = domain_handler.login(user_name, password)
        return [True, user_name_hash]
    except Exception as e:
        logging.error("fail in login: " + e.args[0])
        return [False, e.args[0]]


# 2.5.0
def get_information_about_products(store_name: str):
    """
    Gets all the products of a specific store

    :param store_name: store name
    :return: list of the store products
    """

    try:
        logging.info("get_information_about_products " + store_name)
        ans = domain_handler.get_information_about_products(store_name)
        return [True, ans]
    except Exception as e:
        logging.error("fail: get_information_about_products " + e.args[0])
        return [False, e.args[0]]


# 2.5.1
def get_store_info(store_name: str):
    """
    Get information about specific store (who are the owners contacts and more..)
    :param store_name: store name
    :return: Store
    """
    try:
        logging.info("get_store_info " + store_name)
        ans = domain_handler.get_store_info(store_name)
        return [True, ans]
    except Exception as e:
        logging.error("fail in get_store_info " + e.args[0])
        return [False, e.args[0]]


# TODO DONT NEED THAT NEED TO CHECK WHY THERE IS GET STORE INFO
def get_store(store_name: str):
    """
    Gets a specific store

    :param store_name: store name
    :return: Store
    """

    try:
        logging.info("get store " + store_name)
        ans = domain_handler.get_store(store_name)
        return [True, ans]
    except Exception as e:
        logging.error("get_store failed " + e.args[0])
        return [False, e.args[0]]


def search_product_by_id(product_id):  # 2.6.???? # TODO WHAT IS THIS
    """
    Search a product by his id.

    :param product_id: product id
    :return: Product
    """

    try:
        logging.info("search_product_by_id" + product_id)
        return [True, domain_handler.search_product_by_id(product_id)]
    except Exception as e:
        logging.error("search_product_by_id fail " + e.args[0])
        return [False, e.args[0]]


def find_product_by_id(product_id, store_name):  # TODO SEARCH PRODUCT BY ID IF DECIDED THAT EVERY PRODUCT HAS
    # DIFFERENT ID IS THE SAME NEED TO CHECK
    """
    Search specific product of a specific store
    :param product_id: product id
    :param store_name: store name
    :return: Product
    """

    try:
        logging.info("find_product_by_id: id = " + product_id + "store name = " + store_name)
        return [True, domain_handler.find_product_by_id(product_id, store_name)]
    except Exception as e:
        logging.error("FAIL: id=" + product_id + "store name=" + store_name + " " + e.args[0])
        return [False, "FAIL: id=" + product_id + "store name=" + store_name + " " + e.args[0]]


# 2.6.1
def search_product_by_category(category, filters):
    """
    :param category: product category
    :param filters: filters
    :return: product list
    """
    try:
        logging.info("search_product_by_category: category: " + category)
        return [True, domain_handler.search_product_by_category(category, filters)]
    except Exception as e:
        logging.error("search_product_by_category fail: " + e.args[0])
        return [False, e.args[0]]


# 2.6.2
def search_product_by_name(name, filters):
    """
    :param name: product name
    :param filters: filters
    :return: product list
    """
    try:
        logging.info("starting search product by name: " + name)
        return [True, domain_handler.search_product_by_name(name, filters)]
    except Exception as e:
        return [False, "bug, when searching by name " + e.args[0]]


# 2.6.3

def search_product_by_keyword(keyword, filters):
    """
    :param keyword: product keyword
    :param filters: filters
    :return: product list
    """
    try:
        logging.info("starting search product by keyword: " + keyword)
        return [True, domain_handler.search_product_by_keyword(keyword, filters)]
    except Exception as e:
        logging.error("Error while searching for product by keyword: " + e.args[0])
        return [False, e.args[0]]


# TODO DOESNT NEED THAT FUNCTION MAYBE DELETE?
# 2.7

def save_cart(user_name):
    pass


# 2.8.1

def get_cart_info(user_name):
    """
    Get information about the user cart

    :param user_name: user name
    :return: Cart
    """

    try:
        logging.info("get cart info: user name = " + user_name)
        return [True, domain_handler.get_cart_info(user_name)]
    except Exception as e:
        logging.error("get cart info fail user name = " + user_name + " " + e.args[0])
        return [False, e.args[0]]


"""EDIT THE CART FUNCTIONS"""


# 2.8.2

def add_product_to_cart(user_name, product_id, quantity, store_name):
    """
    Adds a specific product to the user's cart

    :param user_name: user name
    :param product_id: product id
    :param quantity: quantity
    :param store_name: store name
    :return: None
    """

    try:
        logging.info("add product to cart")
        return [True, domain_handler.add_product_to_cart(user_name, product_id, quantity, store_name)]
    except Exception as e:
        logging.error("add product to cart fail: " + e.args[0])
        return [False, e.args[0]]


# 2.8.3

def remove_product_from_cart(user_name, product_id, quantity, store_name):
    """
    Removes the specified quantity from the specific product in the cart

    :param user_name: user name
    :param product_id: product id
    :param quantity: quantity
    :param store_name: store name
    :return: None
    """

    try:
        logging.info("remove product")
        return [True, domain_handler.remove_product_from_cart(user_name, product_id, quantity, store_name)]
    except Exception as e:
        logging.error("remove product fail: " + e.args[0])
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
    payment_done_delivery_done = {"payment_done": False, "delivery_done": False, "quantity_taken": False}

    try:
        logging.info("Starting purchase " + user_name)
        ans = domain_handler.purchase(user_name, payment_info, destination)
        logging.info("Succesful purchase user name = " + user_name)
        return [True, ans]
    except Exception as e:
        logging.error("purchase fail " + e.args[0])
        return [False, e.args[0]]


# 3.1

def logout(user_name):
    """
    Logouts the registered user from the system

    :param user_name: user name
    :return: None
    """

    try:
        logging.info("logout user name: " + user_name)
        domain_handler.logout(user_name)
        return [True, None]
    except Exception as e:
        logging.error("logout fail " + e.args[0])
        return [False, e.args[0]]


# 3.2, think about arguments and preconditions
def open_store(store_name, user_name):
    """
    :param store_name:
    :param user_name:
    :return:
    """
    try:
        logging.info("open_store user name: " + user_name + " store name: " + store_name)
        domain_handler.open_store(store_name, user_name)
        return [True, None]
    except Exception as e:
        logging.error("open_store fail: " + e.args[0])
        return [False, e.args[0]]


# 3.7
def get_user_purchases_history(user_name):
    """
    Gets all user purchase history

    :param user_name:
    :return: list of the purchase history
    """

    try:
        logging.info("get user purchases history: user name: " + user_name)
        return [True, domain_handler.get_user_purchases_history(user_name)]
    except Exception as e:
        logging.error("get user purchases history fail: " + e.args[0])
        return [False, e.args[0]]


# 4.1.1

def add_new_product_to_store_inventory(user_name, product_details, store_name):
    """
    Add new product to specific store's inventory
    :param user_name: user name
    :param product_details: (dict) all the relevant data about the product
    :param store_name: store name
    :return: None
    """
    try:
        logging.info("add_new_product_to_store_inventory: store name: " + store_name)
        domain_handler.add_new_product_to_store_inventory(user_name, product_details, store_name)
        return [True, None]
    except Exception as e:
        logging.error("add_new_product_to_store_inventory fail: " + e.args[0])
        return [False, "Add new product to store inventory fail: " + e.args[0]]


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
        logging.info("remove product from store inventory: product ID: " + product_id)
        domain_handler.remove_product_from_store_inventory(user_name, product_id, store_name)
        return [True, None]
    except Exception as e:
        logging.error("remove product from store inventory fail: " + e.args[0])
        return [False, "remove product from store inventory fail: " + e.args[0]]


# 4.1.3
# maybe change to edit_product
def edit_product_description(user_name: str, product_description: str, store_name: str, product_name: str):
    """
    Edit product description

    :param user_name: user name
    :param product_description: new description
    :param store_name: store name
    :param product_name: product name
    :return: None
    """

    try:
        logging.info("edit_product_details")
        domain_handler.edit_product_description(user_name, product_description, store_name, product_name)
        return [True, None]
    except Exception as e:
        logging.error("edit_product_details fail: " + e.args[0])
        return [False, e.args[0]]


# TODO check if need that function
def edit_product(user_name, product_id, product_name, price, quantity, description, store_name,
                 category, discount_type, buying_type):
    return [False, "Not implemented yet1"]


# 4.3

def assign_store_owner(user_name, new_store_owner_name, store_name):
    """
    Assign new store owner for the store

    :param user_name: user name
    :param new_store_owner_name: the name of the new owner
    :param store_name: store name
    :return: None
    """

    try:
        logging.info("assign store owner")
        domain_handler.assign_store_owner(user_name, new_store_owner_name, store_name)
        return [True, None]
    except Exception as e:
        logging.error("assign store owner fail: " + e.args[0])
        return [False, "assign store owner fail: " + e.args[0]]


# 4.4

def remove_store_owner(user_name: str, store_manager_name: str, store_name: str):
    """
    Removes specific store manager (needs to be assigned by you)

    :param user_name: user name
    :param store_manager_name: store manager name to be deleted
    :param store_name: store name
    :return: None
    """

    try:
        logging.info("remove_store_manager")
        domain_handler.remove_store_manager(user_name, store_manager_name, store_name)
        return True, None
    except Exception as e:
        logging.error("remove_store_manager " + e.args[0])
        return False, e.args[0]


# 4.5

def assign_store_manager(user_name: str, new_store_manager_name: str, store_name: str):
    """
    Assign new store manager to the store

    :param user_name: user name
    :param new_store_manager_name: name of the new store manager
    :param store_name: store name
    :return: None
    """

    try:
        logging.info("assign_store_manager")
        domain_handler.assign_store_manager(user_name, new_store_manager_name, store_name)
        return [True, "New store manager has been added"]
    except Exception as e:
        logging.error("assign store manager failed " + e.args[0])
        return [False, "assign store manager failed " + e.args[0]]


# 4.6

def edit_store_manager_permissions(user_name: str, store_manager_name: str, new_permissions: int, store_name: str):
    """
    Edit the permissions to one of the store manager you assigned

    :param user_name: user name
    :param store_manager_name: The store manager name
    :param new_permissions: int
    :param store_name: store name
    :return: None
    """

    try:
        logging.info("edit_store_manager_permissions")
        domain_handler.edit_store_manager_permissions(user_name, store_manager_name, new_permissions, store_name)
        return [True, None]
    except Exception as e:
        logging.error("edit_store_manager_permissions " + e.args[0])
        return [False, "edit_store_manager_permissions failed " + e.args[0]]


# 4.7

def remove_store_manager(user_name: str, store_manager_name: str, store_name: str):
    """
    Removes specific store manager (needs to be assigned by you)

    :param user_name: user name
    :param store_manager_name: store manager name to be deleted
    :param store_name: store name
    :return: None
    """

    try:
        logging.info("remove_store_manager")
        domain_handler.remove_store_manager(user_name, store_manager_name, store_name)
        return True, None
    except Exception as e:
        logging.error("remove store manager failed" + e.args[0])
        return [False, "remove store manager failed" + e.args[0]]


# 4.9.1

def get_employee_information(user_name: str, employee_name: str, store_name: str):
    """
    Get information about a specific employee

    :param user_name: user name
    :param employee_name: employee name
    :param store_name: store name
    :return: UserDTO
    """

    try:
        logging.info("get_employee_information")
        return [True, domain_handler.get_employee_information(user_name, employee_name, store_name)]
    except Exception as e:
        logging.error("get_employee_information " + e.args[0])
        return [False, "get employee information failed" + e.args[0]]


# 4.9.2

def get_employee_permissions(user_name: str, store_name: str, employee_name: str):
    """
    Get the permissions of a specific employee

    :param user_name: user name
    :param store_name: store name
    :param employee_name: employee name
    :return: The permissions (int)
    """

    try:
        logging.info("get employee permissions")
        return [True, domain_handler.get_employee_permissions(user_name, store_name, employee_name)]
    except Exception as e:
        logging.error("get_employee_permissions " + e.args[0])
        return [False, e.args[0]]


# 4.11

def get_store_purchase_history(user_name, store_name):
    """
    Get the your store purchase history (admins, owners and managers with the right permissions can access it too)

    :param user_name: user name
    :param store_name: store name
    :return: list of purchases
    """

    try:
        logging.info("Get Store purchase history: " + store_name)
        return [True, domain_handler.get_store_purchase_history(user_name, store_name)]
    except Exception as e:
        logging.error("get_store_purchase_history " + e.args[0])
        return [False, e.args[0]]


# 6.4.1

def get_store_purchase_history_admin(user_name, store_name):
    try:
        logging.info("Get Store purchase history admin: " + user_name + " from store: " + store_name)
        return [True, domain_handler.get_store_purchase_history_admin(user_name, store_name)]
    except Exception as e:
        logging.error("Get Store purchase history admin failed due: " + e.args[0])
        return [False, e.args[0]]


# 6.4.2

def get_user_purchase_history_admin(user_name, other_user_name):
    """
    Get user purchase history (only for admins function)

    :param user_name: user name
    :param other_user_name: the user name of the client we want to see his purchase history
    :return:
    """
    try:
        logging.info("Get user purchase history admin: " + user_name + " from user: " + other_user_name)
        return [True, domain_handler.get_user_purchase_history_admin(user_name, other_user_name)]
    except Exception as e:
        logging.error("get_user_purchase_history_admin " + e.args[0])
        return [False, e.args[0]]


def get_store_for_tests(store_id):
    try:
        return [True, domain_handler.get_store_for_tests(store_id)]
    except Exception as e:
        return [False, e.args[0]]


def get_user_for_tests(user_name):
    try:
        return [True, domain_handler.get_user_for_tests(user_name)]
    except Exception as e:
        return [False, e.args[0]]


# we need to implement all those function (4.2)
def get_buying_types(user_name, store_name):
    return [False, "Not implemented yet2"]


def add_buying_types(user_name, store_name, details):
    return [False, "Not implemented yet3"]


def edit_buying_types(user_name, store_name, buying_types, details):
    return [False, "Not implemented yet4"]


def get_discount_types(user_name, store_name):
    return [False, "Not implemented yet5"]


def add_discount_type(user_name, store_name, details):
    return [False, "Not implemented yet6"]


def edit_discount_type(user_name, store_name, discount_type, details):
    return [False, "Not implemented yet7"]


def get_buying_policy(user_name, store_name):
    return [False, "Not implemented yet8"]


def add_buying_policy(user_name, store_name, details):
    return [False, "Not implemented yet9"]


def edit_buying_policy(user_name, store_name, buying_policy, details):
    return [False, "Not implemented yet10"]


def get_discount_policy(user_name, store_name):
    return [False, "Not implemented yet11"]


def edit_discount_policy(user_name, store_name, discount_policy, details):
    return [False, "Not implemented yet12"]


def get_employee_details(user_name, store_name, employeeid):
    return [False, "Not implemented yet13"]


def get_employee_permissions(user_name, store_name, employeeid):
    return [False, "Not implemented yet14"]


def is_user_guest(user_name):
    try:
        # logging.info("add new discount")
        return [True, domain_handler.is_user_guest(user_name)]
    except Exception as e:
        logging.error("is_user_guest " + e.args[0])
        return [False, e.args[0]]


# 4.2
def add_term_discount(user_name, store, discount_name, discount_value, discount_term):
    try:
        logging.info("add new discount")
        return [True, domain_handler.add_term_discount(user_name, store, discount_name, discount_value, discount_term)]
    except Exception as e:
        logging.error("add new discount " + e.args[0])
        return [False, e.args[0]]


def add_simple_discount(user_name, store, discount_name, discount_value):
    try:
        logging.info("add new discount")
        return [True, domain_handler.add_term_discount(user_name, store, discount_name, discount_value)]
    except Exception as e:
        logging.error("add new discount " + e.args[0])
        return [False, e.args[0]]


def add_buying_policy(user_name, store, policy_name: str, s_term: str, no_flag=False):
    try:
        logging.info("add new policy to :" + store + " buy " + user_name)
        return [True, domain_handler.add_policy(user_name, store, policy_name, s_term, no_flag=no_flag)]
    except Exception as e:
        logging.error("add new policy " + e.args[0])
        return [False, e.args[0]]


def delete_buying_policy(user_name, store, policy_name: str):
    try:
        logging.info("delete buying policy")
        return [True, domain_handler.delete_policy(user_name, store, policy_name)]
    except Exception as e:
        logging.error("delete policy " + e.args[0])
        return [False, e.args[0]]


def show_buying_policy(user_name, store):
    try:
        logging.info("show buying policy")
        return [True, domain_handler.show_buying_policy(user_name, store)]
    except Exception as e:
        logging.error("show buying policy " + e.args[0])
        return [False, e.args[0]]


def show_discount_policy(user_name, store):
    try:
        logging.info("show discount policy")
        return [True, domain_handler.show_discount_policy(user_name, store)]
    except Exception as e:
        logging.error("show discount policy " + e.args[0])
        return [False, e.args[0]]


def delete_discount_policy(user_name, store, discount_name):
    try:
        logging.info("delete discount policy")
        return [True, domain_handler.delete_discount_policy(user_name, store, discount_name)]
    except Exception as e:
        logging.error("delete discount policy " + e.args[0])
        return [False, e.args[0]]
