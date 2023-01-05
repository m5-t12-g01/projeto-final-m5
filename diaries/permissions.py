from rest_framework import permissions
from users.models import User
from rest_framework.views import View, Request


class IsPermissionDiary(permissions.BasePermission):
    def has_object_permission(
        self,
        request: Request,
        view: View,
        user: User,
    ) -> bool:
        if request.user.is_authenticated and user == request.user:
            return True
        return False
