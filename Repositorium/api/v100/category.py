from typing import Dict

from rest_framework.viewsets import ViewSet

from repositorium.api.serializers.category import (
    CategoryCreateSerializer,
    CategorySerializer,
)
from repositorium.learning_resources.managers import category as category_manager
from repositorium.utils.mixins import (
    CreateSerializerMixin,
    ListSerializerMixin,
    RetrieveSerializerMixin,
)


class CategoryViewSet(
    CreateSerializerMixin, ListSerializerMixin, RetrieveSerializerMixin, ViewSet
):
    serializer_class = CategorySerializer
    create_serializer_class = CategoryCreateSerializer
    already_exists_errors = {"name": ["Category with that name already exists."]}
    resource_plural_name = "categories"

    def create_object(self, serializer_data: Dict, *args, **kwargs):
        name = serializer_data["name"]
        return category_manager.create_category(name=name)

    def get_objects(self, *args, **kwargs):
        return category_manager.get_all_categories()

    def get_object(self, pk: str, *args, **kwargs):
        return category_manager.get_category_by_uuid(uuid=pk)
