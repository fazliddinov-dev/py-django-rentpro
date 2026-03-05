from rest_framework.exceptions import AuthenticationFailed


class LoginUserUseCase:
    def __init__(self, user_repo, token_service, password_hasher):
        self.user_repo = user_repo
        self.token_service = token_service
        self.password_hasher = password_hasher

    def execute(self, input_dto):
        user = self.user_repo.get_by_email(input_dto.email)

        if not user:
            raise AuthenticationFailed("Invalid credentials")

        if not user.verify_password(input_dto.password, self.password_hasher):
            raise AuthenticationFailed("Invalid credentials")

        token = self.token_service.generate_access_token(user.id)

        return token
