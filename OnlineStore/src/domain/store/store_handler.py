class StoreHandler:
    def __init__(self):
        self.store_dict = dict()  # key-store name value-store

    def get_information_about_products(self, store_name):
        store = self.store_dict[store_name]
        if store is None:
            raise Exception("store name does not exists in the system")
        return store.inventory.product_list

    def get_store_info(self, store_name):
        store = self.store_dict[store_name]
        if store is None:
            raise Exception("store name does not exists in the system")
        return {"store_founder": store.store_founder, "buying_policy": store.buying_policy,
                "buying_types": store.buying_types, "discount_policy": store.discount_policy,
                "discount_types": store.discount_types, }

    def check_product_exists_in_store(self, product_id, store_name):
        store = self.store_dict[store_name]
        if store is None:
            raise Exception("store name does not exists in the system")
        if store.inventory.product_dict[product_id] is None:
            raise Exception("product id does not exists in the store")
