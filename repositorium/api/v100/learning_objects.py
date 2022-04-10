from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from repositorium.utils.mixins import CreateSerializerMixin, ListSerializerMixin


class LearningObjectViewSet(CreateSerializerMixin, ListSerializerMixin, ViewSet):
    def retrieve(self, request: Request, pk: str = None, *args, **kwargs) -> Response:
        pass

    @action(methods=["post"], detail=True, url_name="fork_learning_object")
    def fork(self, request: Request, pk: str = None, *args, **kwargs) -> Response:
        pass

    @action(methods=["post"], detail=True, url_name="rate_learning_object")
    def rate(self, request: Request, pk: str = None, *args, **kwargs) -> Response:
        pass

    @action(methods=["get"], url_name="get_my_learning_objects")
    def my_learning_objects(
        self, request: Request, pk: str = None, *args, **kwargs
    ) -> Response:
        pass
