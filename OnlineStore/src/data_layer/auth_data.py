from pony.orm import db_session

from OnlineStore.src.data_layer import user_entity


@db_session
def add_auth(user_name, password_hash):
    try:
        get_user_auth(user_name)
    except:
        user_entity.UserAuth(user_name=user_name, password_hash=password_hash)
        return
    raise Exception("User Already exists")


@db_session
def remove_auth(user_name):
    try:
        user_entity.UserAuth[user_name].delete()
    except:
        raise Exception("User does not exist")


@db_session
def get_user_auth(user_name):
    """

    :param user_name:
    :return: dict{user_name: str, password_hash: str}
    """
    user_auth = user_entity.UserAuth.get(user_name=user_name)
    if user_auth is None:
        raise Exception("User Does not exist")
    return {"user_name": user_name,
            "password_hash": user_auth.password_hash
            }


@db_session
def user_exist(user_name) -> bool:
    try:
        user_entity.UserAuth[user_name]
        return True
    except:
        return False
