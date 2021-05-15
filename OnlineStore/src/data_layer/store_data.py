from OnlineStore.src.domain_layer.store.store import Store
store_dict = dict()  # key-store name, value-store

def get_store_by_name(store_name: str)->Store:
    store: Store = store_dict.get(store_name)
    if store is None:
        raise Exception("The store {store_name} does not exist in the system!")
    return store

def add_store(new_store: Store)->None:
    global store_dict
    store: Store = store_dict.get(new_store.name)
    if store is not None:
        raise Exception("The store {new_store} already exist in the system!")
    store_dict[new_store.name] = new_store
    
def get_all_stores()->dict:
    return store_dict