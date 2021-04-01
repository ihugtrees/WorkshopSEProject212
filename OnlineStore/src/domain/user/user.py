class User:
    def __init__(self):
        if type(self) is User:
            raise Exception('Base is an abstract class and cannot be instantiated directly')

