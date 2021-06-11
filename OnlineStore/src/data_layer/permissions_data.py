from pony.orm import db_session

from OnlineStore.src.data_layer import user_entity
from OnlineStore.src.domain_layer.permissions.user_permissions import UserPermissions

permissions = dict()  # {user_name: UserPermissions}

@db_session
def get_permissions_by_user_name(user_name: str) -> UserPermissions:
    global permissions
    user_perm = user_entity.User.get(user_name=user_name).userPermissions
    user_permissions = user_entity.User.get(user_name=user_name).permissions
    if user_permissions is None:
        raise Exception("The user does not exist or something went wrong!")
    new_dict = dict()
    for p in user_perm:
        new_dict[p.store_name] = p.store_permmisions
    return UserPermissions(user_name, user_permissions, new_dict)


@db_session
def set_permmisions(new_permissions, user_name, store_name):
    perm_obj = user_entity.UserPermissions.get(user_name=user_name, store_name=store_name)
    if perm_obj is None:
        user_entity.UserPermissions(user_name=user_name, store_name=store_name, store_permissions=new_permissions)
    else:
        perm_obj.store_permissions = new_permissions


@db_session
def remove_employee(store_employee_name, store_name):
    user_entity.UserPermissions.get(user_name=store_employee_name, store_name=store_name).delete()
    user_entity.Appoint.get(user_name=store_employee_name, store_name=store_name).delete()


@db_session
def remove_appointed_by_me(user_name, store_name, the_one_appointed_by_me):
    user_entity.Appoint.get(user_name=user_name, store_name=store_name, appointee=the_one_appointed_by_me).delete()