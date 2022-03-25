from typing import Dict
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from django.core.exceptions import ImproperlyConfigured
from repositorium.utils.exceptions import AlreadyExistsError, DoesNotExistsError
from django.db.models import Model, QuerySet
from django.core.paginator import Paginator, EmptyPage


class SerializerViewSetMixin(object):
    serializer_class: type = None

    def get_serializer_class(self) -> type:
        if self.serializer_class is None:
            raise ImproperlyConfigured(
                f"Missing serializer_class configuration from {self.__class__}"
            )
        return self.serializer_class


class CreateSerializerMixin(SerializerViewSetMixin):
    create_serializer_class: type = None
    already_exists_errors: Dict = None

    def get_create_serializer_class(self) -> type:
        if self.create_serializer_class is None:
            raise ImproperlyConfigured(
                f"Missing create_serializer_class configuration from {self.__class__}"
            )
        return self.create_serializer_class

    def get_already_exists_errors(self) -> Dict:
        if self.already_exists_message is None:
            raise ImproperlyConfigured(
                f"Missing alredy_exists_message configuration from {self.__class__}"
            )
        return self.already_exists_message

    def create_object(self, serializer_data: Dict, *args, **kwargs) -> Model:
        raise ImproperlyConfigured(
            f"Missing definition of create_object method from {self.__class__}"
        )

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_create_serializer_class()(request.data)
        if serializer.is_valid():
            try:
                instance = self.create_object(serializer_data=serializer.data)
            except AlreadyExistsError:
                data = {"errors": self.get_already_exists_errors()}
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
            else:
                instance_serializer = self.get_serializer_class()(instance=instance)
                return Response(
                    data=instance_serializer.data, status=status.HTTP_201_CREATED
                )
        else:
            data = {"errors": serializer.errors}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class ListSerializerMixin(SerializerViewSetMixin):
    resource_plural_name: str = None
    per_page_default: int = 10

    def get_resource_plural_name(self) -> str:
        if self.resource_plural_name is None:
            raise ImproperlyConfigured(
                f"Missing resource_plural_name definition on {self.__class__}"
            )
        return self.resource_plural_name

    def get_objects(self, *args, **kwargs) -> QuerySet:
        raise ImproperlyConfigured(
            f"Define the get_objects method from {self.__class__}"
        )

    def list(self, request: Request, *args, **kwargs) -> Response:
        per_page = request.query_params.get("per_page", self.per_page_default)
        page_number = request.query_params.get("page_number", 1)
        objs = self.get_objects(*args, **kwargs)
        paginator = Paginator(objs, per_page)
        key = self.get_resource_plural_name()
        try:
            page = paginator.get_page(page_number)
        except EmptyPage:
            data = {"page_number": page_number, "has_next_page": False, key: []}
            return Response(status=status.HTTP_204_NO_CONTENT, data=data)
        else:
            serializer = self.get_serializer_class()(page.object_list, many=True)
            data = {
                "page_number": page_number,
                "has_next_page": page.has_next(),
                key: serializer.data,
            }
            return Response(status=status.HTTP_200_OK, data=data)


class RetrieveSerializerMixin(SerializerViewSetMixin):
    def get_object(self, pk: str, *args, **kwargs) -> Model:
        raise ImproperlyConfigured(
            f"Define concrete get_object method on {self.__class__}"
        )

    def retrieve(self, request: Request, pk: str = None, *args, **kwargs) -> Response:
        try:
            obj = self.get_object(pk, *args, **kwargs)
        except DoesNotExistsError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.get_serializer_class()(obj)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
