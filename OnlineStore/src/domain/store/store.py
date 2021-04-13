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
        self.managers = None
        self.owners = None
        self.purchase_history = None
        self.inventory = None
        self.discount_types = None
        self.discount_policy = None
        self.buying_types = None
        self.buying_policy = None
        self.name = store_name
        self.store_founder = store_founder

    def check_permission_to_edit_store_inventory(self, user_name):
        if (user_name not in self.managers) and (user_name not in self.owners) and user_name != self.store_founder:
            raise Exception("current user doesnt have permission to edit the inventory")
