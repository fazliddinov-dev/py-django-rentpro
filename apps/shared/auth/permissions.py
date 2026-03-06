from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user:
            return False

        # Access attribute directly
        return getattr(request.user, "role", None) == "super_admin"
