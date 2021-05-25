from OnlineStore.src.domain_layer.user.user import User

users: dict = dict()
pending_messages: dict = dict()  # key: username, value: list of messages
history_messages: dict = dict()


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


def pop_user_messages(username: str) -> list:
    """

    :param username:
    :return: list of messages (message = {"message": str, "event": str})
    """
    if username not in pending_messages:
        # raise Exception("User does not have messages")
        return list()
    return pending_messages.pop(username)


def add_message(username, message, event) -> None:
    if username not in pending_messages:
        pending_messages[username] = list()
    pending_messages[username].append({"message": message, "event": event})


def add_message_to_history(username, message, event) -> None:
    if username not in history_messages:
        history_messages[username] = list()
    history_messages[username].append({"message": message, "event": event})

