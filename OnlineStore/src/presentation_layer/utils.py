import OnlineStore.src.service_layer.service as service


# logging in
# def check_log_in(username, password):
#     if (username in users and password == users[username]):
#         return True
#     return False

def get_into_site():
    return service.get_into_site()


def exit_the_site(guest_name):
    return service.exit_the_site(guest_name)


def log_in(username, password):
    return service.login(username, password)


def log_out(username):
    return service.logout(username)


# return true for successful sign up
def register(user_name, password, age):
    return service.register(user_name, password, age)


def change_password(user_name, old_password, new_password):
    return service.change_password(user_name, old_password, new_password)


def assign_store_manager(user_name, new_store_manager_name, store_name):
    return service.assign_store_manager(user_name, new_store_manager_name, store_name)


def edit_store_manager_permissions(user_name, store_manager_name, new_permissions, store_name):
    return service.edit_store_manager_permissions(user_name, store_manager_name, new_permissions, store_name)


def remove_store_manager(user_name, store_manager_name, store_name):
    return service.remove_store_manager(user_name, store_manager_name, store_name)


def remove_store_owner(user_name, store_owner_name, store_name):
    return service.remove_store_owner(user_name, store_owner_name, store_name)


def assign_store_owner(user_name, new_store_owner_name, store_name):
    return service.assign_store_owner(user_name, new_store_owner_name, store_name)


def find_product_by_id(product_id, store_name):
    return service.find_product_by_id(product_id, store_name)


def get_store_info(store_name):
    return service.get_store_info(store_name)


def is_user_guest(user_name):  # TODO return admin/store_owner/store_manager/guest
    return service.is_user_guest(user_name)


# return all prodect that match all the filters
def getProductsByFilter(name=None, priceRange=None, rating=None, category=None, storeRating=None, key=None):
    # return service_layer.search_product_by_category(category,filters=)
    # retrun service_layer.search_product_by_name(name, filters=)
    # return service_layer.search_product_by_id(product_id=)
    # return service_layer.search_product_by_keyword(keyword, filters=)
    return "a\nb\nc"


# save user's cart
def save_cart(user_name):
    return service.save_cart(user_name)
    # return True


def get_cart_info(user_name):
    return service.get_cart_info(user_name)
    # return "a b c"


# add product to cart
def add_product_to_cart(user_name, product_id, quantity, store_name):
    return service.add_product_to_cart(user_name, product_id, quantity, store_name)
    # return True


# get total cart price before checkout
def get_cart_info(user_name):
    cart_info = service.get_cart_info(user_name)
    if cart_info[0]:  # bad!!!!!!!!!!!!!!!!!!!!!!!
        return cart_info[1]
    else:
        return cart_info[1]
    # return 10


def purchase(user_name, payment_info, buyer_information):
    return service.purchase(user_name, payment_info, buyer_information)


# def pay(cardNum):
#     return True
#
#
# def checkCartAvailability(user):
#     return True
#
#
# def delivery(user):
#     return True


def remove_product_from_cart(user_name, product_id, quantity, store_name):
    return service.remove_product_from_cart(user_name, product_id, quantity, store_name)
    # return True


# return true if the name is available
# def availableStoreName(storeName):
#     return True


# open new store
def open_store(store_name, user_name):
    return service.open_store(store_name, user_name)
    # return True


def get_user_purchases_history(user_name):
    return service.get_user_purchases_history(user_name)


def get_store_purchase_history(user_name, store_name):
    return service.get_store_purchase_history(user_name, store_name)


def add_new_product_to_store_inventory(user_name, product_id, product_name, price, quantity, description, store_name,
                                       category):
    return service.add_new_product_to_store_inventory(user_name, {"product_id": product_id, "product_name": product_name
        , "quantity": quantity, "description": description, "price": price, "category": category}, store_name)


def remove_product_from_store_inventory(user_name, product_id, store_name):
    return service.remove_product_from_store_inventory(user_name, product_id, store_name)


# TODO implement this func in service_layer
def edit_product(user_name, product_id, product_name, price, quantity, description, store_name,
                 category, discount_type, buying_type):
    return service.edit_product(user_name, product_id, product_name, price, quantity, description, store_name,
                                category, discount_type, buying_type)
    # return True


# TODO we need to implement all those functions in service_layer
def get_buying_types(user_name, store_name):
    return service.get_buying_types(user_name, store_name)


def add_buying_types(user_name, store_name, details):
    return service.add_buying_types(user_name, store_name, details)


def edit_buying_types(user_name, store_name, buying_types, details):
    return service.edit_buying_types(user_name, store_name, buying_types, details)


def get_discount_types(user_name, store_name):
    return service.get_discount_types(user_name, store_name)


def add_discount_type(user_name, store_name, details):
    return service.add_discount_type(user_name, store_name, details)


def edit_discount_type(user_name, store_name, discount_type, details):
    return service.edit_discount_type(user_name, store_name, discount_type, details)


def get_buying_policy(user_name, store_name):
    return service.get_buying_policy(user_name, store_name)


def add_buying_policy(user_name, store_name, policy_name, details):
    return service.add_buying_policy(user_name, store_name, policy_name, details)


def open_product_to_offer(user_name, store_name, product_name, minimum):
    return service.open_product_to_offer(user_name, store_name, product_name, minimum)


def make_offer(user_name, store_name, product_name, quantity, price, payment_detial, buyer_information):
    return service.make_offer(user_name, store_name, product_name, quantity, price, payment_detial, buyer_information)


def delete_buying_policy(user_name, store_name, policy_name):
    return service.delete_buying_policy(user_name, store_name, policy_name)


def delete_discount_policy(user_name, store_name, discount_name):
    return service.delete_discount_policy(user_name, store_name, discount_name)


def get_user_history_message(user_name):
    return service.get_user_history_message(user_name)


def show_buying_policy(user_name, store):
    return service.show_buying_policy(user_name, store)


def show_discount_policy(user_name, store):
    return service.show_discount_policy(user_name, store)


def edit_buying_policy(user_name, store_name, buying_policy, details):
    return edit_buying_policy(user_name, store_name, buying_policy, details)


def get_discount_policy(user_name, store_name):
    return service.get_discount_policy(user_name, store_name)


def edit_discount_policy(user_name, store_name, discount_policy, details):
    return service.edit_discount_policy(user_name, store_name, discount_policy, details)


def add_term_discount(user_name, store_name, discount_name, discount_value, discount_term):
    return service.add_term_discount(user_name, store_name, discount_name, discount_value, discount_term)


def combine_discount(user_name, store_name, discount_name1, discount_name2, operator, new_name):
    return service.combine_discount(user_name, store_name, discount_name1, discount_name2, operator, new_name)


def add_simple_discount(user_name, store_name, discount_name, discount_value):
    return service.add_simple_discount(user_name, store_name, discount_name, discount_value)


def get_employee_details(user_name, store_name, employeeid):
    return service.get_employee_details(user_name, store_name, employeeid)


def get_employee_permissions(user_name, store_name, employeeid):
    return service.get_employee_permissions(user_name, store_name, employeeid)


def userIsStoreOwner(user_hash, store_name):
    return service.is_store_owner(user_hash, store_name)


def userIsStoreManager(user_hash, store_name):
    return service.is_store_manager(user_hash, store_name)


# import OnlineStore.src.service_layer.service as service


# # logging in
# # def check_log_in(username, password):
# #     if (username in users and password == users[username]):
# #         return True
# #     return False

# def log_in(username, password):
#     return service.login(username, password)


# def logout(username):
#     return service.logout(username)


# # return true for successful sign up
# def register(user_name, password):
#     return service.register(user_name, password)


# def assign_store_manager(user_name, new_store_manager_name, store_name):
#     return service.assign_store_manager(user_name, new_store_manager_name, store_name)


# def edit_store_manager_permissions(user_name, store_manager_name, new_permissions, store_name):
#     return service.edit_store_manager_permissions(user_name, store_manager_name, new_permissions, store_name)


# def remove_store_manager(user_name, store_manager_name, store_name):
#     return service.remove_store_manager(user_name, store_manager_name, store_name)


# def remove_store_owner(user_name, store_owner_name, store_name):
#     return service.remove_store_owner(user_name, store_owner_name, store_name)


# def assign_store_owner(user_name, new_store_owner_name, store_name):
#     return service.assign_store_owner(user_name, new_store_owner_name, store_name)


# def find_product_by_id(product_id, store_name):
#     return service.find_product_by_id(product_id, store_name)


# def get_store_info(store_name):
#     return service.get_store_info(store_name)


# def get_user_type(user_name):  # return admin/store_owner/store_manager/guest
#     return "admin"


# # return all prodect that match all the filters
# def getProductsByFilter(name=None, priceRange=None, rating=None, category=None, storeRating=None, key=None):
#     # return service_layer.search_product_by_category(category,filters=)
#     # retrun service_layer.search_product_by_name(name, filters=)
#     # return service_layer.search_product_by_id(product_id=)
#     # return service_layer.search_product_by_keyword(keyword, filters=)
#     return "a\nb\nc"


# # save user's cart
# def save_cart(user_name):
#     return service.save_cart(user_name)
#     # return True


# def get_cart_info(user_name):
#     return service.get_cart_info(user_name)
#     # return "a b c"


# # add product to cart
# def add_product_to_cart(user_name, product_id, quantity, store_name):
#     return service.add_product_to_cart(user_name, product_id, quantity, store_name)
#     # return True


# # get total cart price before checkout
# def get_cart_info(user_name):
#     cart_info = service.get_cart_info(user_name)
#     if cart_info[0]:
#         return cart_info[1]
#     else:
#         return cart_info[1]
#     # return 10


# def purchase(user_name, payment_info, destination):
#     return service.purchase(user_name, payment_info, destination)


# # def pay(cardNum):
# #     return True
# #
# #
# # def checkCartAvailability(user):
# #     return True
# #
# #
# # def delivery(user):
# #     return True


# def remove_product_from_cart(user_name, product_id, quantity, store_name):
#     return service.remove_product_from_cart(user_name, product_id, quantity, store_name)
#     # return True


# # return true if the name is available
# # def availableStoreName(storeName):
# #     return True


# # open new store
# def open_store(store_name, user_name):
#     return service.open_store(store_name, user_name)
#     # return True


# def get_user_purchases_history(user_name):
#     return service.get_user_purchases_history(user_name)
#     # return "dsadsadsa"


# def get_store_purchase_history(user_name, store_name):
#     return service.get_store_purchase_history(user_name, store_name)
#     # return "dsadsadsa"


# def add_new_product_to_store_inventory(user_name, product_id, product_name, price, quantity, description, store_name,
#                                        category, discount_type, buying_type):
#     return service.add_new_product_to_store_inventory(user_name, {"product_id": product_id, "product_name": product_name
#         , "quantity": quantity, "description": description, "price": price, "category": category,
#                                                                   "discount_type": discount_type,
#                                                                   "buying_type": buying_type}, store_name)


# def remove_product_from_store_inventory(user_name, product_id, store_name):
#     return service.remove_product_from_store_inventory(user_name, product_id, store_name)


# # TODO implement this func in service_layer
# def edit_product(user_name, product_id, product_name, price, quantity, description, store_name,
#                  category, discount_type, buying_type):
#     return service.edit_product(user_name, product_id, product_name, price, quantity, description, store_name,
#                                 category, discount_type, buying_type)
#     # return True


# # TODO we need to implement all those functions in service_layer
# def get_buying_types(user_name, store_name):
#     return service.get_buying_types(user_name, store_name)


# def add_buying_types(user_name, store_name, details):
#     return service.add_buying_types(user_name, store_name, details)


# def edit_buying_types(user_name, store_name, buying_types, details):
#     return service.edit_buying_types(user_name, store_name, buying_types, details)


# def get_discount_types(user_name, store_name):
#     return service.get_discount_types(user_name, store_name)


# def add_discount_type(user_name, store_name, details):
#     return service.add_discount_type(user_name, store_name, details)


# def edit_discount_type(user_name, store_name, discount_type, details):
#     return service.edit_discount_type(user_name, store_name, discount_type, details)


# def get_buying_policy(user_name, store_name):
#     return service.get_buying_policy(user_name, store_name)


# def add_buying_policy(user_name, store_name, details):
#     return service.add_buying_policy(user_name, store_name, details)


# def edit_buying_policy(user_name, store_name, buying_policy, details):
#     return edit_buying_policy(user_name, store_name, buying_policy, details)


# def get_discount_policy(user_name, store_name):
#     return service.get_discount_policy(user_name, store_name)


# def edit_discount_policy(user_name, store_name, discount_policy, details):
#     return service.edit_discount_policy(user_name, store_name, discount_policy, details)


# def add_discount_policy(user_name, store_name, details):
#     return service.add_discount_policy(user_name, store_name, details)


# def get_employee_details(user_name, store_name, employeeid):
#     return service.get_employee_details(user_name, store_name, employeeid)


# def get_employee_permissions(user_name, store_name, employeeid):
#     return service.get_employee_permissions(user_name, store_name, employeeid)

def create_filters(minimum, maximum, prating, category, srating):
    if not minimum:
        minimum = 0
    if not maximum:
        maximum = None
    else:
        maximum = float(maximum)
    if not prating:
        prating = 0
    if not srating:
        srating = 0
    return {"min": float(minimum), "max": maximum, "prating": float(prating), "category": category,
            "srating": float(srating)}


def search_product_by_category(category, filters):
    return service.search_product_by_category(category, filters)


def search_product_by_name(name, filters):
    return service.search_product_by_name(name, filters)


def search_product_by_keyword(keyword, filters):
    return service.search_product_by_keyword(keyword, filters)
