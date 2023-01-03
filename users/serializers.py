from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_superuser', 'password', 'username', 'first_name', 'last_name', 'is_adm']
        read_only_fields = ['id', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}