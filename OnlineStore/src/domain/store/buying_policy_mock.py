from OnlineStore.src.dto.user_dto import UserDTO

class BuyingPolicy:
    def __init__(self):
        pass

    def elligible_for_buying(user: UserDTO)->None:
        if user.user_name == "user_name9":
            raise Exception("buying policy fails")
        else:
            return True
