from rest_framework import permissions


class MyCustomPermission(permissions.BasePermission):
    def has_permission(self, req, view):
        if req.method in permissions.SAFE_METHODS:
            return True

        return req.user.is_authenticated and req.user.is_superuser
