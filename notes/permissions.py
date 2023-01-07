from rest_framework import permissions
from notes.models import Note
from rest_framework.views import View, Request


class IsOwnerNote(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Note):
        if request.user.diaries.all().filter(id=obj.diary.id):
            return True
        return False
