from OnlineStore.src.domain.store.inventory import Inventory


class Store:
    def __init__(self, store_name, store_founder, owners=dict(), managers=dict(),
                 buying_policy=None, discount_policy=None, purchase_history=None):
        self.name = store_name
        self.store_founder = store_founder
        self.owners = owners
        self.managers = managers
        self.inventory = Inventory()
        self.buying_policy = buying_policy
        self.discount_policy = discount_policy
        self.purchase_history = purchase_history

    def check_permission_to_edit_store_inventory(self, user_name):
        if (user_name not in self.managers) and (user_name not in self.owners) and user_name != self.store_founder:
            raise Exception("current user doesnt have permission to edit the inventory")

    def remove_product_from_store_inventory(self, product_id):
        self.inventory.remove_product_inventory(product_id)

    def add_new_product_to_store_inventory(self, product_details):
        self.inventory.add_product_inventory(product_details)

    def edit_product(self, product_id, product_details):
        self.inventory.products_dict[product_id].edit_product_description(product_details)

    def check_permission_to_assign(self, user_name):
        if user_name == self.store_founder or user_name in self.owners:
            return True
        return False

    def assign_new_owner(self, owner_name, assign_name):
        if owner_name in self.owners:
            raise Exception(owner_name + "already owner")
        if owner_name in self.managers:
            self.managers.pop(owner_name)
        self.owners[owner_name] = assign_name

    def assign_new_manager(self, manager_name, assign_name):
        if manager_name in self.owners or manager_name in self.managers:
            raise Exception(manager_name + "already owner")
        self.managers[manager_name] = assign_name

    def get_all_assign_of_user(self, user_name):
        all_assign_list = list()
        for user in self.owners:
            if self.owners[user] == user_name:
                all_assign_list.append(user)
        for user in self.managers:
            if self.managers[user] == user_name:
                all_assign_list.append(user)

    def delete_owner_assign(self, user_name_to_delete):
        self.owners.pop(user_name_to_delete)
        for user in self.get_all_assign_of_user(user_name_to_delete):
            self.delete_owner_assign(user)

    def delete_managers(self, user_name_to_delete, user_assign):
        if self.managers[user_name_to_delete] == user_assign:
            self.managers.pop(user_name_to_delete)

    def is_manager_owner(self, user_name, manager_name):
        if self.managers.get(manager_name) is not user_name:
            raise Exception("The user is not the one who assigned the manager")
