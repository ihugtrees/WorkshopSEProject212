from OnlineStore.src.domain_layer.user.user import User
from OnlineStore.src.dto.cart_dto import CartDTO


class UserDTO:
    def __init__(self, user: User):  # change purchase history from none to empty list (yonatan)
        self.user_name = user.user_name
        self.age = user.age
        self.cart = CartDTO(user.cart)
        self.__is_admin = user.is_admin