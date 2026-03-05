from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    """
    Allows access only to users with role 'super_admin' in JWT token.
    """

    def has_permission(self, request, view):
        # DRF SimpleJWT adds user and token to request
        # But since super admin has no DB user, we check token payload manually
        if hasattr(request, "auth") and request.auth:
            role = request.auth.get("role")
            return role == "super_admin"
        return False
