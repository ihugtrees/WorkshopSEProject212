from enum import Enum

class Action(Enum):
    EMPLOYEE_INFO = 0
    EMPLOYEE_PERMISSIONS = 1
    STORE_PURCHASE_HISTORY = 2
    USER_PURCHASE_HISTORY = 3
    LOGOUT = 5
    OPEN_STORE = 6
    CRITIC = 7
    RATE = 8
    MESSAGE = 9
    COMPLAINT = 10
    ADD_MANAGER = 11
    ADD_OWNER = 12
    REMOVE_OWNER = 13
    REMOVE_MANAGER = 14
    ADD_PRODUCT_TO_INVENTORY = 15
    REMOVE_PRODUCT_FROM_INVENTORY = 16
    CLOSE_STORE = 17
    SET_MANAGER_PERMISSIONS = 18
    ADD_DISCOUNT = 19


REGISTERED_PERMMISIONS = (1 << Action.USER_PURCHASE_HISTORY.value | 1 << Action.COMPLAINT.value | 1 << Action.MESSAGE.value |
                                1 << Action.LOGOUT.value | 1 << Action.OPEN_STORE.value | 1 << Action.RATE.value | 1 << Action.CRITIC.value)

GUEST_PERMISSIONS = 0
OWNER_INITIAL_PERMISSSIONS = (1 << Action.EMPLOYEE_INFO.value | 1 << Action.EMPLOYEE_PERMISSIONS.value | 1 << Action.STORE_PURCHASE_HISTORY.value  |
                                 1 << Action.ADD_MANAGER.value | 1 << Action.ADD_OWNER.value | 1 << Action.REMOVE_MANAGER.value | 1 << Action.REMOVE_OWNER.value |
                                  1 << Action.ADD_PRODUCT_TO_INVENTORY.value | 1 << Action.REMOVE_PRODUCT_FROM_INVENTORY.value | 1 << Action.CLOSE_STORE.value |
                                   1 << Action.EMPLOYEE_INFO.value | 1 << Action.SET_MANAGER_PERMISSIONS.value | 1 << Action.ADD_DISCOUNT.value)
MANAGER_INITIAL_PERMISSIONS = (1 << Action.EMPLOYEE_INFO.value | 1 << Action.EMPLOYEE_PERMISSIONS.value )