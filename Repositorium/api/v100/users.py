from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from repositorium.api.serializers.users import UserCreateSerializer, UserSerializer
from repositorium.users import managers as user_manager


class UserViewSet(ViewSet):
    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data["email"]
            password = serializer.data["password"]
            first_name = serializer.data["first_name"]
            last_name = serializer.data["last_name"]
            user = user_manager.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            response_serializer = UserSerializer(instance=user)
            return Response(
                status=status.HTTP_201_CREATED, data=response_serializer.data
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)
