import hashlib
from threading import Lock


class Authentication:
    def __init__(self, passwords=None, users=None, hash_to_name=None, name_to_hash=None):
        self.passwords = passwords if passwords is not None else dict()
        self.users = users if users is not None else dict()  # {"username_hash": loggedIn}
        self._hash_to_name = hash_to_name if hash_to_name is not None else dict()
        self._name_to_hash = name_to_hash if name_to_hash is not None else dict()
        self.lock_reg = Lock()
        self.lock_rest = Lock()

    def register(self, username, password) -> None:
        self.lock_reg.acquire()
        if username in self.passwords:
            self.lock_reg.release()
            raise Exception("User name already exists")
        else:
            self.passwords[username] = hashlib.sha256(password.encode()).hexdigest()
            self.lock_reg.release()
            username_hash = hashlib.sha256(username.encode()).hexdigest()
            self.users[username_hash] = False
            self._hash_to_name[username_hash] = username
            self._name_to_hash[username] = username_hash

    def change_password(self, user_name, old_password, new_password):
        if user_name not in self.passwords.values():
            raise Exception("Error in user session")
        if user_name != hashlib.sha256(old_password.encode()).hexdigest():
            raise Exception("wrong password")
        else:
            self.passwords[self._hash_to_name[user_name]] = hashlib.sha256(new_password.encode()).hexdigest()



    def login(self, username, password) -> str:
        self.lock_rest.acquire()

        if username not in self.passwords:
            self.lock_rest.release()
            raise Exception("User not in the system")
        if self.passwords[username] != hashlib.sha256(password.encode()).hexdigest():
            self.lock_rest.release()
            raise Exception("Password is not correct")
        if self.users[self._name_to_hash[username]] is True:
            self.lock_rest.release()
            raise Exception("User Already Logged In")
        username_hash = hashlib.sha256(username.encode()).hexdigest()
        self.users[username_hash] = True
        self.lock_rest.release()
        return username_hash

    def authenticate_session(self, username_hash):
        self.lock_rest.acquire()
        if username_hash not in self.users:
            self.lock_rest.release()
            raise Exception("Not a user")
        if self.users[username_hash] is False:
            self.lock_rest.release()
            raise Exception("Not Logged In")
        self.lock_rest.release()

    def get_username_from_hash(self, username_hash):
        self.authenticate_session(username_hash)
        return self._hash_to_name[username_hash]

    def logout(self, username_hash):  # TODO MAYBE CHANGE
        self.authenticate_session(username_hash)
        self.users[username_hash] = False

    def guest_registering(self, user_name) -> None:  # TODO MAYBE CHANGE
        self.users[user_name] = True
        self._hash_to_name[user_name] = user_name
        self._name_to_hash[user_name] = user_name

    def check_logged_and_take_lock(self, username) -> Lock:
        """
        Takes the restlock and check if logged in.
        if logged in keep lock and return it
        else release lock and return None
        need to release
        :param username:
        :return: The lock if logged in or None if not logged
        """
        self.lock_rest.acquire()
        if self.users[self._name_to_hash[username]] is True:
            return self.lock_rest
        self.lock_rest.release()
        return None
