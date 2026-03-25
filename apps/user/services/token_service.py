from rest_framework_simplejwt.tokens import RefreshToken


class TokenService:


    @staticmethod
    def issue_tokens(user):

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        return {'access_token': str(access_token), 'refresh_token': str(refresh_token)}