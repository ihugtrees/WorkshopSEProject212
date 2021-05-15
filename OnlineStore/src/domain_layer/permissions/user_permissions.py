from OnlineStore.src.domain_layer.user.action import *

class UserPermissions:
    def __init__(self, user_name: str, permissions: int, permissions_in_store=None):
        self.__user_name = user_name
        self.__permissions = permissions  # guest | registered user | admin permissions
        self.__permissions_in_store = permissions_in_store if permissions_in_store is not None else dict()  # {store_name: myPermissions}
    
    def is_permmited_to(self, action, store_name=None):
        permission_in_store: int = self.__permissions_in_store.get(store_name)
        if (((1 << action) & self.__permissions) == 0) and (permission_in_store is None or ((1 << action) & permission_in_store) == 0):
            raise Exception("Have no permissions to do the action!")
    
    def set_permissions(self, new_permissions: int, store_name: str)->None:
        self.__permissions_in_store[store_name] = new_permissions

    def assign_store_employee(self, new_permissions: int, store_name: str)->None:
        """Adding new permissions to a user for a store. (the user is not an employee of the store yet)

        Args:
            store_name (str): store name
            new_permissions (int): new permissions int representation
        """

        if store_name in self.__permissions_in_store.keys():
            raise Exception("Already is an employee of the store!")
        self.__permissions_in_store[store_name] = new_permissions

    def is_working_in_store(self, store_name: str)->None:
        if store_name not in self.__permissions_in_store.keys():
            raise Exception("The user " + self.__user_name + " is not an employee in " + store_name)

    def remove_employee(self, store_name):
        self.__permissions_in_store.pop(store_name)