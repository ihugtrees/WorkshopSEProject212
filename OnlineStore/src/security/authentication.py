import hashlib
from threading import Lock


class Authentication:
    def __init__(self, passwords=None, users=None, hash_to_name=None):
        self.passwords = passwords if passwords is not None else dict()
        self.users = users if users is not None else dict()  # {"username_hash": loggedIn}
        self._hash_to_name = hash_to_name if hash_to_name is not None else dict()
        self.lock = Lock()

    def register(self, username, password) -> None:
        self.lock.acquire()
        if username in self.passwords:
            self.lock.release()
            raise Exception("User name already exists")
        else:
            self.passwords[username] = hashlib.sha256(password.encode()).hexdigest()
            self.lock.release()
            username_hash = hashlib.sha256(username.encode()).hexdigest()
            self.users[username_hash] = False
            self._hash_to_name[username_hash] = username


    def login(self, username, password) -> str:
        if username not in self.passwords:
            raise Exception("User not in the system")
        if self.passwords[username] != hashlib.sha256(password.encode()).hexdigest():
            raise Exception("Password is not correct")
        username_hash = hashlib.sha256(username.encode()).hexdigest()
        self.users[username_hash] = True
        return username_hash

    def authenticate_session(self, username_hash):
        if username_hash not in self.users:
            raise Exception("Not a user")
        if self.users[username_hash] is False:
            raise Exception("Not Logged In")

    def get_username_from_hash(self, username_hash):
        return self._hash_to_name[username_hash]

    def logout(self, username_hash):  # TODO MAYBE CHANGE
        self.users[username_hash] = False

    def guest_registering(self, user_name) -> None:  # TODO MAYBE CHANGE
        self.users[user_name] = True
        self._hash_to_name[user_name] = user_name
