from typing import List

from rest_framework import serializers

from repositorium.api.serializers.base import BaseSerializer
from repositorium.api.serializers.category import CategorySerializer


class LearningObjectCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True, max_length=125)
    categories = serializers.ListField(child=serializers.CharField())
    system_uuid = serializers.UUIDField()
    extra_data = serializers.JSONField(required=False, default=dict)

    def validate_title(self, value):
        return value.lower()

    def validate_categories(self, value):
        for category in value:
            if "," in category:
                raise serializers.ValidationError("Can't be a ',' in category name")
        return value.lower()


class LearningObjectSerializer(BaseSerializer):
    title = serializers.CharField()
    description = serializers.CharField(allow_blank=True, max_length=125)
    content = serializers.CharField(allow_blank=True)
    categories = CategorySerializer(many=True)
    extra_data = serializers.JSONField()
    creator_email = serializers.EmailField()
    files = serializers.SerializerMethodField()

    # Property
    is_forked = serializers.BooleanField()

    # Method fields
    system = serializers.SerializerMethodField()

    def get_system(self, instance) -> str:
        if instance.created_on is None:
            return ""
        return instance.created_on.name

    def get_files(self, instance) -> List[str]:
        return list(instance.files.values_list("uuid", flat=True))


class LearningObjectForkSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    content = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    categories = serializers.ListField(child=serializers.CharField(), required=False)
    system_uuid = serializers.UUIDField()


class LearningObjectUsageSerializer(BaseSerializer):
    pass
