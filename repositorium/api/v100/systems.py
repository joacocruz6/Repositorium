from typing import Dict

from rest_framework.viewsets import ViewSet

from repositorium.api.serializers.systems import (
    SystemCreateSerializer,
    SystemSerializer,
)
from repositorium.learning_resources.managers import system as system_manager
from repositorium.utils.mixins import (
    CreateSerializerMixin,
    ListSerializerMixin,
    RetrieveSerializerMixin,
)


class SystemViewSet(
    CreateSerializerMixin, ListSerializerMixin, RetrieveSerializerMixin, ViewSet
):
    serializer_class = SystemSerializer
    create_serializer_class = SystemCreateSerializer
    already_exists_errors = {"name": ["System with that name already exists."]}
    resource_plural_name = "systems"

    def create_object(self, serializer_data: Dict, *args, **kwargs):
        name = serializer_data["name"]
        creator_email = self.request.user.email
        return system_manager.create_system(name=name, creator_email=creator_email)

    def get_objects(self, *args, **kwargs):
        return system_manager.get_all_systems()

    def get_object(self, pk: str, *args, **kwargs):
        return system_manager.get_system_by_uuid(uuid=pk)
