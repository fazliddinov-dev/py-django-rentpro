from django.conf import settings

from apps.shared.auth.jwt_utils import create_tokens_for_super_admin


class SuperAdminLoginService:
    def execute(self, username: str, password: str):
        if (
            username == settings.SUPER_ADMIN_USERNAME
            and password == settings.SUPER_ADMIN_PASSWORD
        ):
            return create_tokens_for_super_admin(username)
        return None
