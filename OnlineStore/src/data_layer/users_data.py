from OnlineStore.src.domain.user.user import User

users: dict = dict()


def get_user_by_name(user_name) -> User:
    if user_name not in users:
        raise Exception("user does not exist")
    return users[user_name]


def add_user(user: User) -> None:
    if user.user_name in users:
        raise Exception("user already exists")
    users[user.user_name] = user


def remove_user(user_name: str) -> None:
    if user_name not in users:
        raise Exception("cannot remove: user already does not exist in the system")
    users.pop(user_name)
