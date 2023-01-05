from django.urls import path
from . import views

urlpatterns = [
    path("diaries/", views.DiaryView.as_view())
]