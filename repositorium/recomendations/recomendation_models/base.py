from abc import ABC, abstractmethod

from repositorium.learning_resources.models import LearningObject
from repositorium.recomendations.recomendation_models.filters import base


class BadConfiguredModel(Exception):
    pass


class AbstractRecomendationModel(ABC):
    model_class = None
    model_filter = None

    def __init__(self):
        self.model = None

    def get_model_class(self) -> type:
        if self.model_class is None:
            raise BadConfiguredModel(
                f"Set the attribute 'model_class' on class {self.__class__}"
            )
        return self.model_class

    def get_model_filter(self) -> base.AbstractFilter:
        if self.model_filter is None:
            raise BadConfiguredModel(
                f"Set the attribute 'model_filter' on class {self.__class__}"
            )
        return self.model_filter()

    @abstractmethod
    def load(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def get_recomendation(self, *args, **kwargs) -> LearningObject:
        pass
