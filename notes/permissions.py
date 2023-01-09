from rest_framework import permissions
from notes.models import Note
from rest_framework.views import View, Request


class IsOwnerNote(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, note: Note):
        if request.user.diaries.all().filter(id=note.diary.id):
            return True
        return False
