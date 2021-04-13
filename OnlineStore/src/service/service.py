from OnlineStore.src.domain.user.user_handler import UserHandler
from OnlineStore.src.domain.store.store_handler import StoreHandler
user_handler = UserHandler()
store_handler = StoreHandler()


# 2.1
def get_into_site() -> str:
    return [True, user_handler.get_guest_unique_user_name()]


# 2.2
def exit_the_site(guest_name) -> bool:
    try:
        return [True, user_handler.exit_the_site(guest_name)]
    except Exception as e:
        return [False, e[0]]


# 2.3
def register(user_name, password, first_name, last_name, birthdate):
    try:
        return [True, user_handler.register(user_name, password, first_name, last_name, birthdate)]
    except Exception as e:
        return [False, e[0]]


# 2.4
def login(user_name, password):
    try:
        return [True, user_handler.login(user_name, password)]
    except Exception as e:
        return [False, e[0]]


# 2.5.0
def get_information_about_products(store_name):
    try:
        return [True, store_handler.get_information_about_products(store_name)]
    except Exception as e:
        return [False, e[0]]


# 2.5.1
def get_store_info(store_name):
    try:
        return [True, store_handler.get_store_info(store_name)]
    except Exception as e:
        return [False, e[0]]


# 2.6
def find_products(p_name, category, key_word, filter_options):
    pass


# 2.7
def save_cart(user_name):
    pass


# 2.8.1
def get_cart_info(user_name):
    try:
        return [True, user_handler.get_cart_info(user_name)]
    except Exception as e:
        return [False, e[0]]


"""EDIT THE CART FUNCTIONS"""


# 2.8.2
def add_product(user_name, product_id, quantity, store_name):
    try:
        store_handler.check_product_exists_in_store(product_id, store_name)
        return [True, user_handler.add_product(user_name, product_id, quantity, store_name)]
    except Exception as e:
        return [False, e[0]]


# 2.8.3
def remove_product(user_name, product_id, quantity, store_name):
    try:
        return [True, user_handler.remove_product(user_name, product_id, quantity, store_name)]
    except Exception as e:
        return [False, e[0]]


# 2.9.0
def purchase(user_name, payment_info):
    pass


# 3.1
def logout(user_name):
    pass


# 3.2, think about arguments and preconditions
def open_store(store_name, user_name):
    pass


# 3.7
def get_user_purchases_history(user_name):
    pass


# 4.1.1
def add_new_product_to_store_inventory(user_name, product_details, store_id):
    pass


# 4.1.2
def remove_product_from_store_inventory(user_name, product_id, store_id):
    pass


# 4.1.3
def edit_product_details(user_name, product_details, store_id):
    pass


# 4.3
def assign_store_owner(user_name, new_store_owner_id, store_id):
    pass


# 4.5
def assign_store_manager(user_name, new_store_manager_id, store_id):
    pass


# 4.6
def edit_store_manager_permissions(user_name, new_permissions):
    pass


# 4.7
def remove_store_manager(user_name, store_manager_id):
    pass


# 4.9.1
def get_employee_information(user_name, employee_id):
    pass


# 4.9.2
def get_employee_permissions(user_name, employee_id):
    pass


# 4.11
def get_store_purchase_history(user_name, store_id):
    pass


# 6.4.1
def get_store_purchase_history_admin(user_name, store_id):
    pass


# 6.4.2
def get_user_purchase_history_admin(user_name, other_user_name):
    pass
