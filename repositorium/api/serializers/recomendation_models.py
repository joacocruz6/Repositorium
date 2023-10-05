from typing import List

from rest_framework import serializers


class RecomenderListSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    description = serializers.CharField()


class GetRecomendationSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
