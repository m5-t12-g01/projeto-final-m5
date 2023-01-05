from django.db import models
import uuid


class Diary(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='diaries')
