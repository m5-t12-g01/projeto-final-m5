from .models import User
from rest_framework import permissions
from rest_framework.views import View, Request


class IsSuperUser(permissions.BasePermission):
    def has_permission(
        self,
        request: Request,
        view: View,
    ):
        if request.method not in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_superuser


class UserPermissions(permissions.BasePermission):
    def has_object_permission(
        self,
        request: Request,
        view: View,
        user: User,
    ) -> bool:
        return (
            request.user.is_authenticated
            and request.user.is_superuser
            or user == request.user
        )
