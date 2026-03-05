class User:
    def __init__(self, id: int, username: str, password_hash: str):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def verify_password(self, raw_password: str, hasher):
        return hasher.verify(raw_password, self.password_hash)
