from rest_framework import serializers

from repositorium.api.serializers.base import BaseSerializer
from repositorium.api.serializers.category import CategorySerializer


class LearningObjectCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()
    categories = serializers.ListField(child=serializers.CharField())
    system_uuid = serializers.UUIDField()
    extra_data = serializers.JSONField()


class LearningObjectSerializer(BaseSerializer):
    title = serializers.CharField()
    content = serializers.CharField()
    categories = CategorySerializer(many=True)
    extra_data = serializers.JSONField()
    creator_email = serializers.EmailField()

    # Property
    is_forked = serializers.BooleanField()

    # Method fields
    system = serializers.SerializerMethodField()

    def get_system(self, instance) -> str:
        if instance.created_on is None:
            return ""
        return instance.created_on.name


class LearningObjectForkSerializer(serializers.Serializer):
    system_uuid = serializers.UUIDField()


class LearningObjectUsageSerializer(BaseSerializer):
    pass
