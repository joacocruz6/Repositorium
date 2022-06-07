from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from repositorium.api.serializers.users import (
    LoginSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from repositorium.users import managers as user_manager


class UserViewSet(ViewSet):
    @action(
        methods=["post"], detail=False, url_name="create", permission_classes=[AllowAny]
    )
    def create_user(self, request: Request, *args, **kwargs) -> Response:
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

    @action(methods=["get"], detail=False, url_name="session")
    def current_user(self, request: Request, *args, **kwargs):
        serializer = UserSerializer(instance=request.user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(methods=["put"], detail=False, url_name="change_password")
    def change_password(self, request: Request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    @action(methods=["put"], detail=False, url_name="update_user")
    def update_user(self, request: Request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)


class AuthViewSet(ViewSet):
    @action(methods=["post"], detail=False, url_name="login")
    @permission_classes([AllowAny])
    def login(self, request: Request, *args, **kwargs) -> Response:
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data["email"]
            password = serializer.data["password"]
            user = authenticate(email=email, password=password)
            if user is None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            token = Token.objects.create(user=user)
            data = {
                "auth_token": token.key,
            }
            return Response(status=status.HTTP_200_OK, data=data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=False, url_name="logout")
    @permission_classes([IsAuthenticated])
    def logout(self, request: Request, *args, **kwargs):
        user = request.user
        auth_token = request.auth
        token = Token.objects.get(user=user, key=auth_token)
        token.delete()
        return Response(status=status.HTTP_200_OK)
