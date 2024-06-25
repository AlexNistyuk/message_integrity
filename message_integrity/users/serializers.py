from rest_framework import serializers
from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "email_type",
        )

        read_only_fields = ("id",)

        extra_kwargs = {"password": {"write_only": True}}
