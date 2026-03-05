class LoginInputDTO:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password


class LoginOutputDTO:
    def __init__(self, access_token: str):
        self.access_token = access_token
