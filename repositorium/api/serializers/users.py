from typing import Any, Dict

from django.utils.html import conditional_escape
from rest_framework import serializers

from repositorium.users import managers as user_manager


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=150, min_length=8)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    def validate_email(self, value: str):
        return value.lower()

    def validate_first_name(self, value):
        return conditional_escape(value)

    def validate_last_name(self, value):
        return conditional_escape(value)

    def validate(self, data):
        email = data["email"]
        if user_manager.check_user_exists(email=email):
            raise serializers.ValidationError("User already exists")
        return data


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    uuid = serializers.UUIDField()
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    created_at = serializers.DateTimeField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, value: str):
        return value.lower()


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=150)
    new_password = serializers.CharField(max_length=150, min_length=8)
    confirm_new_password = serializers.CharField(max_length=150)

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError("New password confirmation didn't match")
        return data


class UpdateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
