from rest_framework import serializers


class ExperimentSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()


class FinishExperimentSerializer(serializers.Serializer):
    model = serializers.UUIDField()
    item = serializers.UUIDField()
