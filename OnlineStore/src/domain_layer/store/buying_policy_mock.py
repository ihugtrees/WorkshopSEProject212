from OnlineStore.src.dto.user_dto import UserDTO

class BuyingPolicyMock:
    def __init__(self):
        pass

    def eligible_for_buying(self, user: UserDTO, basketDTO )->None:
        if user.user_name == "user_name9":
            raise Exception("buying policy fails")
        else:
            return True
