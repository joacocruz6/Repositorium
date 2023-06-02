from abc import ABC, abstractmethod

from django.db.models import QuerySet


class AbstractFilter(ABC):
    @abstractmethod
    def get_objects(self, *args, **kwargs) -> QuerySet:
        pass
