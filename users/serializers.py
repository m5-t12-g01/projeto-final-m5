from rest_framework import serializers
from .models import User
from send_email.views import send_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "is_superuser",
            "password",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_adm",
        ]
        read_only_fields = ["id", "is_superuser"]
        extra_kwargs = {
            "password": {"write_only": True},
            "is_adm": {
                "default": False,
            },
        }

    def create(self, validated_data: dict) -> User:
        send_email(
            validated_data["first_name"],
            validated_data["last_name"],
            validated_data["email"],
        )

        if validated_data["is_adm"]:
            return User.objects.create_superuser(**validated_data)

        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance
