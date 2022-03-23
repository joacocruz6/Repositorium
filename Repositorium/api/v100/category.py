from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from repositorium.api.serializers.category import (
    CategorySerializer,
    CategoryCreateSerializer,
)


class CategoryViewSet(ViewSet):
    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = CategoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.data["name"]

    def list(self, request: Request) -> Response:
        pass

    def retrieve(self, request: Request, pk: str = None) -> Response:
        pass
