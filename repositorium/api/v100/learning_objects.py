from typing import Dict

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from repositorium.api.serializers.learning_object import (
    LearningObjectCreateSerializer,
    LearningObjectSerializer,
)
from repositorium.learning_resources.exceptions import SystemDoesNotExists
from repositorium.learning_resources.managers import category as category_manager
from repositorium.learning_resources.managers import (
    learning_objects as learning_object_manager,
)
from repositorium.learning_resources.managers import system as system_manager
from repositorium.learning_resources.models import LearningObject
from repositorium.utils.mixins import (
    CreateSerializerMixin,
    ListSerializerMixin,
    RetrieveSerializerMixin,
)


class LearningObjectViewSet(
    CreateSerializerMixin, ListSerializerMixin, RetrieveSerializerMixin, ViewSet
):
    serializer_class = LearningObjectSerializer
    create_serializer_class = LearningObjectCreateSerializer
    already_exists_errors = {
        "title": ["Learning object with that title already exists."]
    }
    resource_plural_name = "learning_objects"

    def create_object(self, serializer_data: Dict, *args, **kwargs) -> LearningObject:
        title = serializer_data["title"]
        content = serializer_data["content"]
        category_names = serializer_data["categories"]
        system_uuid = serializer_data["system_uuid"]
        extra_data = serializer_data["extra_data"]
        creator = self.request.user

        system = system_manager.get_system_by_uuid(uuid=system_uuid)
        categories, _ = category_manager.get_or_create_categories(
            category_names=category_names
        )
        learning_object = learning_object_manager.create_learning_object(
            title=title,
            content=content,
            categories=categories,
            created_on=system,
            created_by=creator,
            extra_data=extra_data,
        )
        return learning_object

    def create(self, request: Request, *args, **kwargs) -> Response:
        try:
            return super().create(request, *args, **kwargs)
        except SystemDoesNotExists:
            data = {
                "errors": {
                    "system_uuid": ["System with submitted uuid does not exists."]
                }
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    @action(methods=["post"], detail=True, url_name="fork_learning_object")
    def fork(self, request: Request, pk: str = None, *args, **kwargs) -> Response:
        pass

    @action(methods=["post"], detail=True, url_name="rate_learning_object")
    def rate(self, request: Request, pk: str = None, *args, **kwargs) -> Response:
        pass

    @action(methods=["get"], url_name="get_my_learning_objects")
    def my_learning_objects(
        self, request: Request, pk: str = None, *args, **kwargs
    ) -> Response:
        pass
