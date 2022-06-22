from django.core.paginator import EmptyPage, Paginator
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from repositorium.api.serializers.learning_object import LearningObjectSerializer
from repositorium.learning_resources.managers import category as category_manager
from repositorium.learning_resources.managers import (
    learning_objects as learning_object_manager,
)


class RecomenderViewSet(ViewSet):
    def list(self, request: Request, *args, **kwargs) -> Response:
        category_names = request.query_params.get("categories", [])
        page_number = request.query_params.get("page_number", 1)
        per_page = request.query_params.get("per_page", 10)
        categories_uuids = category_manager.get_category_uuids_by_names(
            category_names=category_names
        )
        learning_objects = (
            learning_object_manager.get_learning_objects_by_category_uuids(
                categories_uuids=categories_uuids
            )
        )
        paginator = Paginator(learning_objects)
        try:
            page = paginator.get_page()
        except EmptyPage:
            data = {
                "page_number": page_number,
                "has_next_page": False,
                "learning_objects": [],
            }
            return Response(status=status.HTTP_204_NO_CONTENT, data=data)
        else:
            serializer = LearningObjectSerializer(page.object_list, many=True)
            data = {
                "page_number": page_number,
                "has_next_page": page.has_next(),
                "learning_objects": serializer.data,
            }
            return Response(status=status.HTTP_200_OK, data=data)
