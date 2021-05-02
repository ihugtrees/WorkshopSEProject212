from OnlineStore.src.domain.adapters import payment_adapter, supply_adapter
from OnlineStore.src.domain.user.action import Action
from OnlineStore.src.domain.user.user_handler import UserHandler
from OnlineStore.src.domain.store.store_handler import StoreHandler
from OnlineStore.src.security.authentication import Authentication
from OnlineStore.src.domain.permissions.permission_handler import PermissionHandler
import OnlineStore.src.data_layer.purchase_data as purchase_handler
import OnlineStore.src.domain.user.action as action
import OnlineStore.src.data_layer.users_data as users
import OnlineStore.src.data_layer.store_data as stores
from OnlineStore.src.service.logger import Logger

user_handler = UserHandler()
store_handler = StoreHandler()
permission_handler = PermissionHandler()
auth = Authentication()
logging = Logger()


# 2.1

def get_into_site():
    """
    Should call this function right when entering the site
    register the new client as a guest

    :return: guest username
    """

    ans = user_handler.get_guest_unique_user_name()
    auth.guest_registering(ans)
    return ans

# 2.2

def exit_the_site(guest_name):
    """
    Should call when leaving the site. Unregisteres the guest user and delete all his info

    :param guest_name: guest name
    :return: None
    """

    return user_handler.exit_the_site(guest_name)

# 2.3

def register(user_name: str, password: str):
    """
    Registeres new user to the system

    :param user_name: user name
    :param password: password
    :return: None
    """

    auth.register(user_name, password)
    user_handler.register(user_name)

# 2.4

def login(user_name: str, password: str):
    """
    Login registered user to the system

    :param user_name: user name
    :param password: password
    :return: hashed user name (function as a session key)
    """

    user_name_hash = auth.login(user_name, password)
    user_handler.login(user_name)
    return user_name_hash

# 2.5.0

def get_information_about_products(store_name: str):
    """
    Gets all the products of a specific store

    :param store_name: store name
    :return: list of the store products
    """

    return store_handler.get_information_about_products(store_name)

# 2.5.1

def get_store_info(store_name: str):
    """
    Get information about specific store (who are the owners contacts and more..)

    :param store_name: store name
    :return: Store
    """

    return store_handler.get_store_info(store_name)

# TODO DONT NEED THAT NEED TO CHECK WHY THERE IS GET STORE INFO

def get_store(store_name: str):
    """
    Gets a specific store

    :param store_name: store name
    :return: Store
    """
    return store_handler.get_store(store_name)


def search_product_by_id(product_id):  # 2.6.???? # TODO WHAT IS THIS
    """
    Search a product by his id.

    :param product_id: product id
    :return: Product
    """

    for store in stores.get_all_stores().values():
        if product_id in store.inventory.products_dict:
            ans = store.inventory.products_dict[product_id]
            return ans
    raise Exception("product not found")


def find_product_by_id(product_id, store_name):  # TODO SEARCH PRODUCT BY ID IF DECIDED THAT EVERY PRODUCT HAS
    # DIFFERENT ID IS THE SAME NEED TO CHECK
    """
    Search specific product of a specific store
    :param product_id: product id
    :param store_name: store name
    :return: Product
    """

    return store_handler.find_product_by_id(product_id, store_name)

# 2.6.1

def search_product_by_category(category, filters):
    """
    :param category: product category
    :param filters: filters
    :return: product list
    """

    return store_handler.search_product_by_category(category, filters)

# 2.6.2

def search_product_by_name(name, filters):
    """
    Search specific product of a specific store

    :param name: product name
    :param filters: filters
    :return: product list
    """
    return store_handler.search_product_by_name(name, filters)

# 2.6.3

def search_product_by_keyword(keyword, filters):
    """
    :param keyword: product keyword
    :param filters: filters
    :return: product list
    """
    product_list = store_handler.search_product_by_keyword(keyword, filters)
    if len(product_list) == 0:
        raise Exception("Product not found")
    return product_list

# TODO DOESNT NEED THAT FUNCTION MAYBE DELETE?
# 2.7

def save_cart(user_name):
    pass

# 2.8.1

def get_cart_info(user_name):
    """
    Get information about the user cart

    :param user_name: user name
    :return: CartDTO
    """

    user_name = auth.get_username_from_hash(user_name)
    return user_handler.get_cart_info(user_name)

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

    user_name = auth.get_username_from_hash(user_name)
    store_handler.check_product_exists_in_store(product_id, store_name)
    return user_handler.add_product(user_name, store_name, product_id, quantity)

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
    user_name = auth.get_username_from_hash(user_name)
    return user_handler.remove_product(user_name, product_id, quantity, store_name)

# 2.9.0

def purchase(user_name: str, payment_info: dict, destination: str):
    """
    Purchase all the items in the cart

    :param delivery_success:
    :param payment_success:
    :param destination: the address of the customer
    :param user_name: user name
    :param payment_info: {credit_num: str, three_digits: str, expiration_date: date}
    :return: [boolean, T] -> if boolean is false T is a string representation of the problem if boolean is true T is expected time of delivery
    """
    payment_done_delivery_done = {"payment_done": False, "delivery_done": False, "quantity_taken": False}

    try:
        user_name = auth.get_username_from_hash(user_name)
        user_dto = user_handler.get_user_dto_by_name(user_name)
        cart_dto = user_dto.cart
        store_handler.is_valid_for_purchase(cart_dto, user_dto)
        store_handler.take_quantity(cart_dto)
        payment_done_delivery_done["quantity_taken"] = True
        cart_sum = store_handler.calculate_cart_sum(cart_dto)
        payment_adapter.pay_for_cart(payment_info, cart_sum)
        date = supply_adapter.supply_products_to_user(cart_dto, destination)
        user_handler.empty_cart(user_name)
        purchase_handler.add_all_basket_purchases_to_history(cart_dto, user_name)
        return date
    except Exception as e:
        if payment_done_delivery_done["quantity_taken"]:
            store_handler.return_quantity(cart_dto)
            payment_done_delivery_done["quantity_taken"] = False
        if payment_done_delivery_done["payment_done"]:
            payment_adapter.return_for_cart(payment_info, cart_sum)
            payment_done_delivery_done["payment_done"] = False
        raise Exception(e.args[0])

# 3.1

def logout(user_name):
    """
    Logouts the registered user from the system

    :param user_name: user name
    :return: None
    """

    hash_user_name = user_name
    user_name = auth.get_username_from_hash(user_name)
    permission_handler.is_permmited_to(user_name=user_name, action=Action.LOGOUT.value)
    auth.logout(hash_user_name)
    user_handler.logout(user_name)

# 3.2, think about arguments and preconditions

def open_store(store_name, user_name):
    """

    :param store_name:
    :param user_name:
    :return: None
    """

    user_name = auth.get_username_from_hash(user_name)
    permission_handler.is_permmited_to(user_name=user_name, action=Action.OPEN_STORE.value)
    user_handler.check_permission_to_open_store(
        user_name)  # just checks if user is logged in need to see if to change name
    store_handler.open_store(store_name, user_name)
    permission_handler.set_permissions(action.OWNER_INITIAL_PERMISSSIONS, user_name, store_name)

# 3.7

def get_user_purchases_history(user_name):
    """
    Gets all user purchase history

    :param user_name:
    :return: list of the purchase history
    """

    user_name = auth.get_username_from_hash(user_name)
    return purchase_handler.get_user_purchases(user_name)

# 4.1.1

def add_new_product_to_store_inventory(user_name, product_details, store_name):
    """
    Add new product to specific store's inventory

    :param user_name: user name
    :param product_details: (dict) all the relevant data about the product
    :param store_name: store name
    :return: None
    """

    user_name = auth.get_username_from_hash(user_name)
    permission_handler.is_permmited_to(user_name, Action.ADD_PRODUCT_TO_INVENTORY.value,
                                                        store_name)
    store_handler.add_new_product_to_store_inventory(user_name, product_details, store_name)

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

    user_name = auth.get_username_from_hash(user_name)
    permission_handler.is_permmited_to(user_name, Action.REMOVE_PRODUCT_FROM_INVENTORY.value,
                                                        store_name)
    store_handler.remove_product_from_store_inventory(user_name, product_id, store_name)


# 4.1.3

def edit_product_description(user_name: str, product_description: str, store_name: str, product_name: str):
    """
    Edit product description

    :param user_name: user name
    :param product_description: new description
    :param store_name: store name
    :param product_name: product name
    :return: None
    """

    user_name = auth.get_username_from_hash(user_name)
    permission_handler.is_permmited_to(user_name=user_name,
                                                        action=Action.ADD_PRODUCT_TO_INVENTORY.value,
                                                        store_name=store_name)
    stores.get_store_by_name(store_name).edit_product(product_name,
                                                            product_description)  # TODO CHANGE THIS

# 4.3

def assign_store_owner(user_name, new_store_owner_name, store_name):
    """
    Assign new store owner for the store

    :param user_name: user name
    :param new_store_owner_name: the name of the new owner
    :param store_name: store name
    :return: None
    """

    user_name = auth.get_username_from_hash(user_name)
    permission_handler.is_permmited_to(user_name, Action.ADD_OWNER.value, store_name)
    permission_handler.assign_store_employee(action.OWNER_INITIAL_PERMISSSIONS,
                                                            new_store_owner_name,
                                                            store_name)
    user_handler.assign_store_employee(user_name, new_store_owner_name, store_name)
# 4.5

def assign_store_manager(user_name: str, new_store_manager_name: str, store_name: str):
    """
    Assign new store manager to the store

    :param user_name: user name
    :param new_store_manager_name: name of the new store manager
    :param store_name: store name
    :return: None
    """

    user_name = auth.get_username_from_hash(user_name)
    permission_handler.is_permmited_to(user_name, Action.ADD_MANAGER.value, store_name)
    permission_handler.assign_store_employee(action.MANAGER_INITIAL_PERMISSIONS,
                                                            new_store_manager_name,
                                                            store_name)
    user_handler.assign_store_employee(user_name, new_store_manager_name, store_name)

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

    user_name = auth.get_username_from_hash(user_name)
    permission_handler.is_permmited_to(user_name, Action.SET_MANAGER_PERMISSIONS.value,
                                                        store_name)
    user_handler.is_assigned_by_me(user_name, store_manager_name, store_name)
    permission_handler.set_permissions(action.OWNER_INITIAL_PERMISSSIONS & new_permissions,
                                                        store_manager_name,
                                                        store_name)

# 4.7

def remove_store_manager(user_name: str, store_manager_name: str, store_name: str):
    """
    Removes specific store manager (needs to be assigned by you)

    :param user_name: user name
    :param store_manager_name: store manager name to be deleted
    :param store_name: store name
    :return: None
    """

    user_name = auth.get_username_from_hash(user_name)
    permission_handler.is_permmited_to(user_name, Action.REMOVE_MANAGER.value, store_name)
    user_handler.remove_employee(user_name, store_manager_name, store_name)

# 4.9.1

def get_employee_information(user_name: str, employee_name: str, store_name: str):
    """
    Get information about a specific employee

    :param user_name: user name
    :param employee_name: employee name
    :param store_name: store name
    :return: UserDTO
    """

    user_name = auth.get_username_from_hash(user_name)
    permission_handler.is_permmited_to(user_name=user_name, action=Action.EMPLOYEE_INFO.value,
                                                        store_name=store_name)
    permission_handler.is_working_in_store(employee_name, store_name)
    return user_handler.get_employee_information(employee_name)

# 4.9.2

def get_employee_permissions(user_name: str, store_name: str, employee_name: str):
    """
    Get the permissions of a specific employee

    :param user_name: user name
    :param store_name: store name
    :param employee_name: employee name
    :return: The permissions (int)
    """
    user_name = auth.get_username_from_hash(user_name)
    permission_handler.is_permmited_to(user_name, Action.EMPLOYEE_PERMISSIONS, store_name)
    permission_handler.is_working_in_store(employee_name, store_name)
    return user_handler.get_employee_information(
        employee_name)  # TODO FOR NOW RETURN INFORMATION MAYBE TO CHANGE TO NEW FUNCTION

# 4.11

def get_store_purchase_history(user_name, store_name):
    """
    Get the your store purchase history (admins, owners and managers with the right permissions can access it too)

    :param user_name: user name
    :param store_name: store name
    :return: list of purchases
    """

    user_name = auth.get_username_from_hash(user_name)
    permission_handler.is_permmited_to(user_name, Action.STORE_PURCHASE_HISTORY.value, store_name)
    return purchase_handler.get_store_purchases(store_name)

# 6.4.1

def get_store_purchase_history_admin(user_name, store_name):
    return get_store_purchase_history(user_name, store_name)

# 6.4.2

def get_user_purchase_history_admin(user_name, other_user_name):
    """
    Get user purchase history (only for admins function)

    :param user_name: user name
    :param other_user_name: the user name of the client we want to see his purchase history
    :return:
    """

    user_name = auth.get_username_from_hash(user_name)
    # user_handler.is_permitted_to_do(user_name, None, 1 << Action.USER_PURCHASE_HISTORY.value)
    # check if admin
    return purchase_handler.get_user_purchases(other_user_name)


def get_store_for_tests(store_id):
    return stores.get_store_by_name(store_id)


def get_user_for_tests(user_name):
    user_name = auth.get_username_from_hash(user_name)
    return users.get_user_by_name(user_name)