from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user:
            return False

        return request.user.get("role") == "super_admin"
