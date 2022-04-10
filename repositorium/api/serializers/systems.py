from rest_framework import serializers

from repositorium.api.serializers.base import BaseSerializer


class SystemSerializer(BaseSerializer):
    name = serializers.CharField(max_length=150)


class SystemCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)

    def validate_name(self, value: str) -> str:
        return value.capitalize()
