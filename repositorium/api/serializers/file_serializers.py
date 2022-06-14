from rest_framework import serializers

from repositorium.api.serializers.base import BaseSerializer


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class LearningObjectFileSerializer(BaseSerializer):
    file_route = serializers.FilePathField()
    learning_object_uuid = serializers.SerializerMethodField()

    def get_learning_object_uuid(self, instance) -> str:
        return str(instance.learning_object.uuid)
