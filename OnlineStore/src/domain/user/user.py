from OnlineStore.src.domain.user.cart import Cart
from OnlineStore.src.domain.user.user_handler import Action


class User:
    def __init__(self, user_name: str, cart: Cart, is_admin=False,
                 purchase_history=list()):  # change purchase history from none to empty list (yonatan)
        self.is_logged = False
        self.user_name = user_name
        self.cart = cart
        self.__is_admin = is_admin
        self.purchase_history = purchase_history
        self.permissions = dict()  # {str(store_name): int}

    def login(self):
        if self.is_logged:
            raise Exception("Already loggedIn")
        self.is_logged = True

    def logout(self):
        self.is_logged = False

    def is_admin(self):
        return self.__is_admin

    def add_product_to_user(self, store, product_id: int, quantity: int):
        self.cart.add_product_to_cart(store, product_id, quantity)

    def remove_product_from_user(self, store, product_id: int, quantity: int):
        self.cart.remove_product_from_cart(store, product_id, quantity)

    def edit_store_manager_permissions(self, store_name: str, new_permissions: int):
        if self.permissions.get(store_name) is None:
            raise Exception("The user is not a manager in the store")
        self.permissions[store_name] = new_permissions

    def is_permitted_to_do(self, action: int, store_name: str):
        if self.__is_admin is False and (action & self.permissions.get(store_name)) is 0:
            raise Exception("The User does not have the permission to do the action")
        if self.__is_admin is True and (
                action is not 1 << Action.STORE_PURCHASE_HISTORY or action is not 1 << Action.USER_HISTORY):
            raise Exception("Admin doesnt have permission to do so")
