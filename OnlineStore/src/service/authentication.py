import hashlib


class Authentication:
    def __init__(self, data=None):
        if data is None:
            data = dict()
        self.users = data

    def register(self, username, password):
        if username in self.users:
            return -1
        else:
            self.users[username] = hashlib.sha256(password.encode()).hexdigest()
            return 1

    def login(self, username, password):
        if username in self.users and self.users[username] == hashlib.sha256(password.encode()).hexdigest():
            return 1
        else:
            return -1
