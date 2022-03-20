from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    created_at = serializers.DateTimeField()
