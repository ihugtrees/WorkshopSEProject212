import hashlib
from threading import Lock

import OnlineStore.src.data_layer.auth_data as auth_data


class Authentication:
    def __init__(self, passwords=None, users=None, hash_to_name=None, name_to_hash=None):
        self.passwords = passwords if passwords is not None else dict()
        self.users = users if users is not None else dict()  # {"username_hash": loggedIn}
        self._hash_to_name = hash_to_name if hash_to_name is not None else dict()
        self._name_to_hash = name_to_hash if name_to_hash is not None else dict()
        self.lock_reg = Lock()
        self.lock_rest = Lock()

    def register(self, username, password) -> None:
        username_hash = hashlib.sha256(username.encode()).hexdigest()
        self.lock_reg.acquire()
        if username in self.passwords or auth_data.user_exist(username_hash):
            self.lock_reg.release()
            raise Exception("User name already exists")
        else:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            try:
                auth_data.add_auth(username, password_hash)
            except Exception as e:
                self.lock_reg.release()
                raise e
            self.passwords[username] = password_hash
            self.lock_reg.release()
            self.users[username_hash] = False
            self._hash_to_name[username_hash] = username
            self._name_to_hash[username] = username_hash

    def change_password(self, user_name, old_password, new_password):
        user_name = self._hash_to_name[user_name]
        if user_name not in self.passwords or not auth_data.user_exist(user_name=user_name):
            raise Exception("Error in user session")
        if self.passwords[user_name] != hashlib.sha256(old_password.encode()).hexdigest():
            raise Exception("wrong password")
        else:
            self.passwords[user_name] = hashlib.sha256(new_password.encode()).hexdigest()
            auth_data.remove_auth(user_name)
            auth_data.add_auth(user_name,  self.passwords[user_name])

    def login(self, username, password) -> str:
        self.lock_rest.acquire()
        if not auth_data.user_exist(user_name=username):
            self.lock_rest.release()
            raise Exception("User does not exist in the system")
        if username not in self.passwords.keys():
            self.__set_auth_from_db(username)
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
            raise Exception("Something went wrong try to login again or User does not exist in the system")
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
        auth_data.add_auth(user_name, user_name)

    def remove_guest(self, guest_name: str):
        self.users.pop(guest_name)
        self._hash_to_name.pop(guest_name)
        self._name_to_hash.pop(guest_name)
        auth_data.remove_auth(guest_name)

    def check_logged_and_take_lock(self, username) -> Lock:
        """
        Takes the restlock and check if logged in.
        if logged in keep lock and return it
        else release lock and return None
        need to release
        :param username:
        :return: The lock if logged in or None if not logged
        """
        try:
            self.lock_rest.acquire()
            if self.users[self._name_to_hash[username]] is True:
                return self.lock_rest
            self.lock_rest.release()
            return None
        except:
            self.lock_rest.release()
            return None

    def __set_auth_from_db(self, username):
        auth_dict = auth_data.get_user_auth(user_name=username)
        self.passwords[auth_dict["user_name"]] = auth_dict["password_hash"]
        username_hash = hashlib.sha256(username.encode()).hexdigest()
        self.users[username_hash] = False
        self._hash_to_name[username_hash] = username
        self._name_to_hash[username] = username_hash
