

class Event:
    def __init__(self, func_name: str, args: list, return_value):
        self.func_name = func_name
        self.args = args
        self.return_value = return_value
