from typing import List

from django.db.models import QuerySet

from repositorium.learning_resources.managers import (
    learning_objects as learning_objects_manager,
)
from repositorium.recomendations.recomendation_models.filters import base


class ItemCategoriesBasicFilter(base.AbstractFilter):
    def get_objects(self, item_uuid: str, *args, **kwargs) -> QuerySet:
        main_learning_resource = learning_objects_manager.get_learning_object_by_uuid(
            uuid=item_uuid
        )
        category_names = main_learning_resource.categories.values_list(
            "name", flat=True
        )
        return learning_objects_manager.get_learning_objects_with_categories(
            category_names=category_names
        ).exclude(uuid=item_uuid)
