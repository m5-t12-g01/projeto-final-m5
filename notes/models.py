from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid


class Note(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    priority = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(3),
        ],
        default=2,
    )

    diary = models.ForeignKey(
        "diaries.Diary",
        on_delete=models.CASCADE,
        related_name="notes",
    )
