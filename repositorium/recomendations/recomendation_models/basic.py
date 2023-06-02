from repositorium.learning_resources.models import LearningObject
from repositorium.recomendations.recomendation_models import base


class SimpleLastCreatedRecomendation(base.AbstractRecomendationModel):
    def load(self, *args, **kwargs):
        pass

    def get_recomendation(self, *args, **kwargs) -> LearningObject:
        return LearningObject.objects.order_by("-created_at").first()
