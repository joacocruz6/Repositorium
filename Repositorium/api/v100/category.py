from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from repositorium.api.serializers.category import (
    CategorySerializer,
    CategoryCreateSerializer,
)
from repositorium.learning_resources.managers import category as category_manager
from repositorium.learning_resources.exceptions import (
    CategoryAlreadyExists,
    CategoryDoesNotExists,
)
from django.core.paginator import Paginator, EmptyPage


class CategoryViewSet(ViewSet):
    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = CategoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.data["name"]
            try:
                category = category_manager.create_category(name=name)
            except CategoryAlreadyExists:
                data = {"errors": {"name": ["Category already exists."]}}
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
            else:
                category_serializer = CategorySerializer(instance=category)
                return Response(
                    status=status.HTTP_201_CREATED, data=category_serializer.data
                )
        else:
            data = {"errors": serializer.errors}
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)

    def list(self, request: Request, *args, **kwargs) -> Response:
        per_page = request.query_params.get("per_page", 10)
        page_number = request.query_params.get("page_number", 1)
        categories = category_manager.get_all_categories()
        paginator = Paginator(categories, per_page)
        try:
            page = paginator.get_page(page_number)
        except EmptyPage:
            data = {
                "page_number": page_number,
                "has_next_page": False,
                "categories": [],
            }
            return Response(status=status.HTTP_204_NO_CONTENT, data=data)
        else:
            serializer = CategorySerializer(page.object_list, many=True)
            data = {
                "page_number": page_number,
                "has_next_page": page.has_next,
                "categories": serializer.data,
            }
            return Response(status=status.HTTP_200_OK, data=data)

    def retrieve(self, request: Request, pk: str = None, *args, **kwargs) -> Response:
        try:
            category = category_manager.get_category(name=pk)
        except CategoryDoesNotExists:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = CategorySerializer(category)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
