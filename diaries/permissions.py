from rest_framework import permissions
from diaries.models import Diary
from rest_framework.views import View, Request

class IsPermissionDiary(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Diary):
        if request.user.is_authenticated and obj.user == request.user:
            return True
        return False
