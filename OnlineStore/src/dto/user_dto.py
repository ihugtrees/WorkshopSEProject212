from OnlineStore.src.domain.user.user import User
from OnlineStore.src.dto.cart_dto import CartDTO


class UserDTO:
    def __init__(self, user: User):  # change purchase history from none to empty list (yonatan)
        self.is_logged = user.is_logged
        self.user_name = user.user_name
        self.cart = CartDTO(user.cart)
        self.__is_admin = user.is_admin
        self.purchase_history = user.purchase_history
        self.permissions = user.permissions  # {str(store_name): int}