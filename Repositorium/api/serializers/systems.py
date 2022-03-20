from rest_framework import serializers
from repositorium.api.serializers.base import BaseSerializer


class SystemSerializer(BaseSerializer):
    name = serializers.CharField(max_length=150)


class SystemCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
