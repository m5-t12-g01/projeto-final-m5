from django.db import models
import uuid


class NotePriority(models.TextChoices):
    HIGH = "High"
    AVERAGE = "Average"
    LOW = "Low"


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

    priority = models.CharField(
        max_length=20,
        null=True,
        choices=NotePriority.choices,
        default=NotePriority.AVERAGE,
    )

    diary = models.ForeignKey(
        "diaries.Diary",
        on_delete=models.CASCADE,
        related_name="notes",
    )
