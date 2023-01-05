from django.urls import path
from . import views

urlpatterns = [
    path("diaries/", views.DiaryView.as_view()),
    path("diaries/<uuid:pk>/", views.DiaryDetailView.as_view()),
]
