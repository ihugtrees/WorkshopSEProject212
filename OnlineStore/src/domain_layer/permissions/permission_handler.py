import OnlineStore.src.data_layer.permissions_data as permissions
from OnlineStore.src.domain_layer.permissions.user_permissions import UserPermissions


class PermissionHandler:
    def __init__(self):
        pass

    def is_permmited_to(self, user_name: str, action: int, store_name=None) -> None:
        """Check if the user is permitted to do the action.
        Raise an error if the user has not permission to do the action.

        Args:
            user (UserDTO): The user that asks to do the action.
            action (int): The action num (from Action) the user wants to do.
            :param user_name:
            :param store_name:
        """

        user_permissions: UserPermissions = permissions.get_permissions_by_user_name(user_name)
        user_permissions.is_permmited_to(action, store_name)

    def set_permissions(self, new_permissions: int, user_name: str, store_name: str) -> None:
        permissions.get_permissions_by_user_name(user_name).set_permissions(new_permissions, store_name)

    def assign_store_employee(self, new_permissions: int, user_name: str, store_name: str) -> None:
        permissions.get_permissions_by_user_name(user_name).assign_store_employee(new_permissions, store_name)

    def is_working_in_store(self, user_name: str, store_name: str) -> None:
        permissions.get_permissions_by_user_name(user_name).is_working_in_store(store_name)

    def remove_employee(self, to_remove: list, store_name: str):
        for store_employee_name in to_remove:
            permissions.get_permissions_by_user_name(store_employee_name).remove_employee(store_name)

    # TODO MAYBE CHANGE TO GET ROLE IN STORE
    def is_store_owner(self, user_name, store_name):
        """
        Raises an exception if not store owner

        Args:
            user_name (str):
            store_name (str):
        """
        permissions.get_permissions_by_user_name(user_name).is_store_owner(store_name)

    
    # TODO MAYBE CHANGE TO GET ROLE IN STORE
    def is_store_manager(self, user_name, store_name):
        """
        Raises an exception if not store manager

        Args:
            user_name (str):
            store_name (str):
        """
        permissions.get_permissions_by_user_name(user_name).is_store_manager(store_name)