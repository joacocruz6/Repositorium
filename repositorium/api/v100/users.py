from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from repositorium.api.serializers.users import (
    ChangePasswordSerializer,
    LoginSerializer,
    UpdateUserSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from repositorium.users import managers as user_manager
from repositorium.users.exceptions import (
    ChangePasswordException,
    MultipleUsersReturned,
    UserAlreadyExists,
    UserDoesNotExists,
)


class UserViewSet(ViewSet):
    @action(
        methods=["post"],
        detail=False,
        url_path="create",
        url_name="create",
        permission_classes=[AllowAny],
    )
    def create_user(self, request: Request, *args, **kwargs) -> Response:
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data["email"]
            password = serializer.data["password"]
            first_name = serializer.data["first_name"]
            last_name = serializer.data["last_name"]
            try:
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
            except UserAlreadyExists:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], detail=False, url_path="current", url_name="session")
    def current_user(self, request: Request, *args, **kwargs):
        serializer = UserSerializer(instance=request.user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(methods=["put"], detail=False, url_name="change_password")
    def change_password(self, request: Request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            current_password = serializer.data["current_password"]
            new_password = serializer.data["new_password"]
            try:
                user_manager.change_user_password(
                    user=request.user,
                    current_password=current_password,
                    new_password=new_password,
                )
            except ChangePasswordException:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

    @action(methods=["put"], detail=False, url_path="update", url_name="update_user")
    def update_user(self, request: Request, *args, **kwargs):
        serializer = UpdateUserSerializer(data=request.user)
        if serializer.is_valid():
            first_name = serializer.get("first_name", request.user.first_name)
            last_name = serializer.get("last_name", request.user.last_name)
            try:
                user_manager.update_user(
                    user_email=request.user.email,
                    first_name=first_name,
                    last_name=last_name,
                )
                request.user.refresh_from_db()
                serialized_user = UserSerializer(instance=request.user)
                return Response(status=status.HTTP_200_OK, data=serialized_user.data)
            except (UserDoesNotExists, MultipleUsersReturned):
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AuthViewSet(ViewSet):
    @action(
        methods=["post"], detail=False, url_name="login", permission_classes=[AllowAny]
    )
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

    @action(
        methods=["post"],
        detail=False,
        url_name="logout",
        permission_classes=[IsAuthenticated],
    )
    def logout(self, request: Request, *args, **kwargs):
        user = request.user
        auth_token = request.auth
        token = Token.objects.get(user=user, key=auth_token)
        token.delete()
        return Response(status=status.HTTP_200_OK)
