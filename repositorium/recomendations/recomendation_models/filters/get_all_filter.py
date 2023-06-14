from django.db.models import QuerySet

from repositorium.learning_resources.models import LearningObject
from repositorium.recomendations.recomendation_models.filters import base


class GetAllFilter(base.AbstractFilter):
    def filter(self, *args, **kwargs) -> QuerySet:
        return LearningObject.objects.all()
