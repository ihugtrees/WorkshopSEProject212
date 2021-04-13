class Store:
    def __init__(self, name, buying_policy, buying_types, discount_policy,
                 discount_types, inventory, purchase_history, owners, managers, store_founder):
        self.managers = managers
        self.owners = owners
        self.purchase_history = purchase_history
        self.inventory = inventory
        self.discount_types = discount_types
        self.discount_policy = discount_policy
        self.buying_types = buying_types
        self.buying_policy = buying_policy
        self.name = name
        self.store_founder = store_founder
