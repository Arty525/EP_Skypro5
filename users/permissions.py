from rest_framework.permissions import BasePermission


class IsCurrentUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj or request.user.is_superuser:
            return True
        return False
