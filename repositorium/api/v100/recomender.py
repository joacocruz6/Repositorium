from django.db.models import QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from repositorium.api.serializers.learning_object import LearningObjectSerializer
from repositorium.api.serializers.recomendation_models import (
    GetRecomendationSerializer,
    RecomenderListSerializer,
)
from repositorium.recomendations.recomendation_models import (
    manager as recomendation_model_manager,
)
from repositorium.utils.mixins import ListSerializerMixin


class RecomenderViewSet(ListSerializerMixin, ViewSet):
    serializer_class = RecomenderListSerializer
    resource_plural_name = "recomendation_models"

    def get_objects(self, request: Request, *args, **kwargs) -> QuerySet:
        recomendation_models = (
            recomendation_model_manager.get_all_recomendation_models()
        )
        return [recomendation_models[key] for key in recomendation_models]

    @action(methods=["post"], detail=True, url_name="get_recomendation")
    def get_recomendation(
        self, request: Request, pk: str = None, *args, **kwargs
    ) -> Response:
        serializer = GetRecomendationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                model = recomendation_model_manager.get_recomendation_model_by_uuid(
                    uuid=pk
                )
                recomendation = model.get_recomendation(serializer.data["uuid"])
                recomendation_serializer = LearningObjectSerializer(
                    instance=recomendation
                )
                return Response(
                    status=status.HTTP_200_OK, data=recomendation_serializer.data
                )
            except recomendation_model_manager.RecomendationModelNotFound:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
