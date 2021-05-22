class Appoint:
    def __init__(self, appointed_by_me=None):
        self.__appointed_by_me = appointed_by_me if appointed_by_me is not None else dict()  # {store_name: (list[str] = list of all appointees}

    def is_appointed_by_me(self, store_name: str, appointee: str):
        appointees: list = self.__appointed_by_me[store_name]
        if appointees is None or appointee not in appointees:
            raise Exception("The user " + appointee + " not appointed by you!")

    def assign_store_employee(self, new_store_owner_name: str, store_name: str) -> None:
        if self.__appointed_by_me.get(store_name) is None:
            self.__appointed_by_me[store_name] = list()
        self.__appointed_by_me[store_name].append(new_store_owner_name)

    def remove_appointed(self, store_employee: str, store_name: str) -> None:
        self.__appointed_by_me[store_name].remove(store_employee)

    def get_all_appointed(self, store_name: str) -> list:
        return self.__appointed_by_me[store_name] if store_name in self.__appointed_by_me.keys() else list()

    def remove_store_from_appoint(self, store_name):
        try:
            self.__appointed_by_me.pop(store_name)
        except Exception as e:
            return
