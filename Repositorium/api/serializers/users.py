from rest_framework import serializers
from django.utils.html import conditional_escape
from repositorium.api.serializers.base import BaseSerializer


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=150, min_length=8)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    def validate_first_name(self, value):
        return conditional_escape(value)

    def last_name(self, value):
        return conditional_escape(value)


class UserSerializer(BaseSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
