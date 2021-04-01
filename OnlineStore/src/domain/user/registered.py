from OnlineStore.src.domain.user.user import User


class Registered(User):
    cartList = list()

    def __init__(self, username, password):
        self.username = username
        self.password = password
