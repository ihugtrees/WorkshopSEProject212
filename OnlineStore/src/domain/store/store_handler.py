from OnlineStore.src.domain.store.store import Store


class StoreHandler:
    def __init__(self):
        self.store_dict = dict()

    def create_store(self, name):
        self.store_dict[name] = Store(name)

    def print_stores(self):
        print(self.store_dict)
