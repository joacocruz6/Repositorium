from rest_framework import serializers

from repositorium.api.serializers.base import BaseSerializer


class CategorySerializer(BaseSerializer):
    name = serializers.CharField(max_length=150)


class CategoryCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)

    def validate_name(self, value: str) -> str:
        return value.capitalize()
