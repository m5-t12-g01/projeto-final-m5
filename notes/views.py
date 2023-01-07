from .models import Note
from diaries.models import Diary
from .serializers import NoteSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from diaries.permissions import IsPermissionDiary
from notes.permissions import IsOwnerNote
from django.shortcuts import get_object_or_404


class NoteView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsPermissionDiary]

    serializer_class = NoteSerializer

    def get_queryset(self):

        route_parameter = self.request.GET.get("priority")

        diary_id = self.kwargs["pk"]
        diary_obj = get_object_or_404(Diary, pk=diary_id)
        self.check_object_permissions(self.request, diary_obj)

        if route_parameter:
            return (
                Note.objects.all()
                .filter(diary=diary_obj)
                .filter(priority__icontains=route_parameter)
            )

        return Note.objects.all().filter(diary=diary_obj).order_by("-priority")

    def perform_create(self, serializer):
        diary_id = self.kwargs["pk"]
        diary_obj = get_object_or_404(Diary, pk=diary_id)
        self.check_object_permissions(self.request, diary_obj)
        serializer.save(diary_id=self.kwargs.get("pk"))


class NoteDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerNote]

    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    lookup_url_kwarg = "pk"
