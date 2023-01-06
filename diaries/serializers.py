from rest_framework import serializers
from .models import Diary


class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ["id", "name", "user_id", "created_at"]
        read_only_fields = ["created_at"]
