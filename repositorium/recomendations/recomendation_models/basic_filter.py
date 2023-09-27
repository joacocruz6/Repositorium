from django.db.models import QuerySet

from repositorium.learning_resources.models import LearningObject, LearningObjectUsage
from repositorium.recomendations.recomendation_models import base
from repositorium.recomendations.recomendation_models.filters.user_used_filter import (
    UserSeenFilter,
)
from repositorium.users import managers as user_manager


class ProfileLastFilteredModel(base.AbstractRecomendationModel):
    model_filter = UserSeenFilter

    def load(self, *args, **kwargs) -> None:
        pass

    def get_recomendation(self, user_uuid: str, *args, **kwargs) -> LearningObject:
        learning_objects = self.get_model_filter().get_objects(user_uuid=user_uuid)
        return learning_objects.order_by("-created_at").first()
