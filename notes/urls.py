from django.urls import path
from . import views

urlpatterns = [
    path("diaries/<uuid:diary_id>/notes/", views.NoteView.as_view()),
    path("notes/<uuid:note_id>/", views.NoteDetailView.as_view()),
]
