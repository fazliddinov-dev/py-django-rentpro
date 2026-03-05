class LoginInputDTO:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


class LoginOutputDTO:
    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token
