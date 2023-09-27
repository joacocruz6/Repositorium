from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from repositorium.api.serializers.experiment import (
    ExperimentSerializer,
    FinishExperimentSerializer,
)
from repositorium.recomendations.exceptions import ExperimentNotFoundError
from repositorium.recomendations.managers import experiment as experiment_manager


class ExperimentViewSet(ViewSet):
    def create(self, request: Request, *args, **kwargs) -> Response:
        experiment = experiment_manager.create_experiment(user=request.user)
        serializer = ExperimentSerializer(instance=experiment)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, pk=None, *args, **kwargs) -> Response:
        serializer = FinishExperimentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                experiment_manager.finish_experiment(
                    uuid=pk,
                    user_uuid=request.user.uuid,
                    model_uuid=serializer.data["model"],
                    item_recommended_uuid=serializer.data["item"],
                )
                return Response(status=status.HTTP_200_OK)
            except ExperimentNotFoundError:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            data = {
                "errors": "missing some values on the request. Check to include both values."
            }
            return Response(status=status.HTTP_400_BAD_REQUEST)
