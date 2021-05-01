from OnlineStore.src.domain.permissions.user_permissions import UserPermissions

permissions =  dict()  #{user_name: UserPermissions}

def get_permissions_by_user_name(user_name: str)->UserPermissions:
    global permissions
    user_permissions: UserPermissions = permissions[user_name]
    if user_permissions is None:
        raise Exception("The user does not exist or something went wrong!")
    return user_permissions 

def add_permission(user_name: str, perm: int)->None:
    global permissions
    permissions[user_name] = UserPermissions(user_name, perm)