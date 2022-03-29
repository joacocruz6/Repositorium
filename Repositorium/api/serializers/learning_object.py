from rest_framework import serializers

from repositorium.api.serializers.base import BaseSerializer
from repositorium.api.serializers.category import CategorySerializer


class LearningObjectListSerializer(BaseSerializer):
    name = serializers.CharField()
    categories = CategorySerializer(many=True)
    creator_name = serializers.SerializerMethodField()

    def get_creator_name(self, instance) -> str:
        return instance.created_by.full_name
