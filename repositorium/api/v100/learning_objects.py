from typing import Dict

from django.core.paginator import EmptyPage, Paginator
from django.db.models import Model, QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from repositorium.api.serializers.learning_object import (
    LearningObjectCreateSerializer,
    LearningObjectForkSerializer,
    LearningObjectSerializer,
)
from repositorium.learning_resources.exceptions import (
    LearningObjectDoesNotExists,
    SystemDoesNotExists,
)
from repositorium.learning_resources.managers import category as category_manager
from repositorium.learning_resources.managers import (
    learning_objects as learning_object_manager,
)
from repositorium.learning_resources.managers import (
    learning_objects as learning_objects_manager,
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

    def get_object(self, pk: str, *args, **kwargs) -> Model:
        return learning_objects_manager.get_learning_object_by_uuid(uuid=pk)

    def get_objects(self, *args, **kwargs) -> QuerySet:
        return learning_objects_manager.get_all_learning_objects()

    def create_object(self, serializer_data: Dict, *args, **kwargs) -> LearningObject:
        title = serializer_data["title"]
        content = serializer_data["content"]
        category_names = serializer_data["categories"]
        system_uuid = serializer_data["system_uuid"]
        extra_data = serializer_data["extra_data"]
        creator_email = self.request.user.email

        system = system_manager.get_system_by_uuid(uuid=system_uuid)
        categories, _ = category_manager.get_or_create_categories(
            category_names=category_names
        )
        learning_object = learning_object_manager.create_learning_object(
            title=title,
            content=content,
            categories=categories,
            created_on=system,
            creator_email=creator_email,
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
        serializer = LearningObjectForkSerializer(data=request.data)
        if serializer.is_valid():
            system_uuid = serializer.data["system_uuid"]
            try:
                system = system_manager.get_system_by_uuid(uuid=system_uuid)
                forked_by = request.user
                original_learning_object = (
                    learning_object_manager.get_learning_object_by_uuid(uuid=pk)
                )
                learning_object = learning_object_manager.fork_learning_object(
                    original_learning_object=original_learning_object,
                    forked_by=forked_by,
                    forked_on=system,
                )
                learning_object_serializer = self.get_serializer_class()(
                    instance=learning_object
                )
                return Response(
                    data=learning_object_serializer.data, status=status.HTTP_201_CREATED
                )
            except SystemDoesNotExists:
                data = {
                    "errors": {"system_uuid": ["System with that uuid does not exist."]}
                }
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)
            except LearningObjectDoesNotExists:
                data = {
                    "errors": {
                        "learning_object": [
                            "Learning object with that uuid does not exist."
                        ]
                    },
                }
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        else:
            data = {"errors": serializer.errors}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=True, url_name="rate_learning_object")
    def rate(self, request: Request, pk: str = None, *args, **kwargs) -> Response:
        return Response(status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False, url_name="get_my_learning_objects")
    def my_learning_objects(self, request: Request, *args, **kwargs) -> Response:
        per_page = request.query_params.get("per_page", self.per_page_default)
        page_number = request.query_params.get("page_number", 1)
        learning_objects = self.get_objects()
        learning_objects = learning_objects.filter(
            creator_email=request.user.email
        ).order_by("-created_at")
        paginator = Paginator(learning_objects, per_page)
        key = self.get_resource_plural_name()
        try:
            page = paginator.get_page(page_number)
        except EmptyPage:
            data = {"page_number": page_number, "has_next_page": False, key: []}
            return Response(status=status.HTTP_204_NO_CONTENT, data=data)
        else:
            serializer = self.get_serializer_class()(page.object_list, many=True)
            data = {
                "page_number": page_number,
                "has_next_page": page.has_next(),
                key: serializer.data,
            }
            return Response(status=status.HTTP_200_OK, data=data)
