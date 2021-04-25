from OnlineStore.src.domain.store.inventory import Inventory
from OnlineStore.src.domain.user.basket import Basket
from OnlineStore.src.domain.user.user import User


class Store:
    def __init__(self, store_name, store_founder, owners=None, managers=None,
                 buying_policy=None, discount_policy=None, purchase_history=None):
        self.name = store_name
        self.store_founder = store_founder
        self.owners = owners if owners is not None else dict()  # key-username, val-assigner:str
        self.managers = managers if managers is not None else dict()  # key-username, val-assigner:str
        self.inventory = Inventory(dict())
        self.buying_policy = buying_policy
        self.discount_policy = discount_policy
        self.purchase_history = purchase_history
        self.rating = 0

    def check_permission_to_edit_store_inventory(self, user_name):
        if (user_name not in self.managers) and (user_name not in self.owners) and user_name != self.store_founder:
            raise Exception("current user doesnt have permission to edit the inventory")
        else:
            return True

    def remove_product_store(self, product_id):
        self.inventory.remove_product_inventory(product_id)

    def add_product_store(self, product_details):
        self.inventory.add_product_inventory(product_details)

    def edit_product(self, product_id, product_details):
        if product_id not in self.inventory.products_dict:
            raise Exception("cant edit non existent product")
        self.inventory.products_dict[product_id].edit_product_description(product_details)

    def check_permission_to_assign(self, user_name):
        if user_name != self.store_founder and user_name not in self.owners:
            raise Exception("permission denied")

    def assign_new_owner(self, new_owner, assigner):
        if new_owner in self.owners:
            raise Exception(new_owner + "already owner")
        if new_owner in self.managers:
            self.managers.pop(new_owner)
        self.owners[new_owner] = assigner

    def assign_new_manager(self, new_manager, assigner):
        if new_manager in self.owners or new_manager in self.managers:
            raise Exception(new_manager + "already owner or manager")
        self.managers[new_manager] = assigner

    def __get_assigns_of_user(self, assigner):
        all_assign_list = list()
        for owner in self.owners:
            if self.owners[owner] == assigner:
                all_assign_list.append(owner)
        for manager in self.managers:
            if self.managers[manager] == assigner:
                all_assign_list.append(manager)

    def delete_owner(self, user_name_to_delete):
        self.owners.pop(user_name_to_delete)
        for user in self.__get_assigns_of_user(user_name_to_delete):
            self.delete_owner(user)

    # def is_manager_owner(self, user_name, manager_name):
    #     if self.managers.get(manager_name) is not user_name:
    #         raise Exception("The user is not the one who assigned the manager")

    def is_policies_eligible(self, user: User):  # TODO
        pass

    def calculate_basket_sum(self, basket: Basket) -> int:
        basket_sum = 0
        for product_name in basket.products_dict.keys():
            basket_sum += self.inventory.products_dict.get(product_name).calculate_product_sum(
                basket.products_dict.get(product_name))

        return basket_sum

    def delete_manager(self, user_name_to_delete, assigner):
        if self.managers[user_name_to_delete] != assigner:
            raise Exception("Only assigner can delete his manager")
        self.managers.pop(user_name_to_delete)

    # def is_manager_owner(self, user_name, manager_name):
    #     if self.managers.get(manager_name) is not user_name:
    #         raise Exception("The user is not the one who assigned the manager")
