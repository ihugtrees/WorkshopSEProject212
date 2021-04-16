from OnlineStore.src.domain.store.inventory import Inventory


class Store:
    def __init__(self, store_name, buying_policy, buying_types, discount_policy,
                 discount_types, inventory, purchase_history, owners, managers, store_founder):
        self.managers = managers
        self.owners = owners
        self.purchase_history = purchase_history
        self.inventory = inventory
        self.discount_types = discount_types
        self.discount_policy = discount_policy
        self.buying_types = buying_types
        self.buying_policy = buying_policy
        self.name = store_name
        self.store_founder = store_founder

    def __init__(self, store_name, store_founder):
        self.managers = dict()
        self.owners = dict()
        self.purchase_history = None
        self.inventory = Inventory(dict())
        self.discount_types = None
        self.discount_policy = None
        self.buying_types = None
        self.buying_policy = None
        self.name = store_name
        self.store_founder = store_founder

    def check_permission_to_edit_store_inventory(self, user_name):
        if (user_name not in self.managers) and (user_name not in self.owners) and user_name != self.store_founder:
            raise Exception("current user doesnt have permission to edit the inventory")

    def remove_product_from_store_inventory(self, product_id):
        self.inventory.remove_product_from_store_inventory(product_id)

    def add_new_product_to_store_inventory(self, product_details):
        self.inventory.add_new_product_to_store_inventory(product_details)

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

    def is_manager_owner(self, user_name, manager_name):
        if self.managers.get(manager_name) is not user_name:
            raise Exception("The user is not the one who assigned the manager")
