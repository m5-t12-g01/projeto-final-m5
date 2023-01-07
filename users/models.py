import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=50, unique=True, error_messages={'unique':'A user with that username already exists.'})
    email = models.EmailField(max_length=150, unique=True, error_messages={'unique':'A user with this email already exists.'})
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_adm = models.BooleanField(default=False)

