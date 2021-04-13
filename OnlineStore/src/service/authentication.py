import hashlib


class Authentication:
    def __init__(self, data=None):
        if data is None:
            data = dict()
        self.users = data

    def register(self, username, password):
        if username in self.users:
            return False
        else:
            self.users[username] = hashlib.sha256(password.encode()).hexdigest()
            return True

    def login(self, username, password):
        if username in self.users and self.users[username] == hashlib.sha256(password.encode()).hexdigest():
            return True
        else:
            return False
