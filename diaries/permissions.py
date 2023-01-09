from rest_framework import permissions
from diaries.models import Diary
from rest_framework.views import View, Request


class IsPermissionDiary(permissions.BasePermission):
    def has_object_permission(
        self,
        request: Request,
        view: View,
        diary: Diary,
    ):
        if request.user.is_authenticated and diary.user == request.user:
            return True
        return False
