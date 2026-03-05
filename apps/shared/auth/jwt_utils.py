from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


def create_tokens_for_super_admin(username: str):
    """
    Manually create JWT tokens for super admin
    """
    # Create refresh token
    refresh = RefreshToken()
    refresh["username"] = username
    refresh["role"] = "super_admin"

    # Create access token from refresh
    access = refresh.access_token

    return {
        "access": str(access),
        "refresh": str(refresh),
        "role": "super_admin",
    }
