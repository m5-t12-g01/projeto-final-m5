from django.urls import path
from . import views

urlpatterns = [
    path("diaries/<uuid:pk>/notes/", views.NoteView.as_view()),
    path("notes/<uuid:pk>/", views.NoteDetailsView.as_view()),
]
