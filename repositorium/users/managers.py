from typing import Union
from uuid import UUID

from repositorium.users.exceptions import (
    ChangePasswordException,
    MultipleUsersReturned,
    UserDoesNotExists,
)
from repositorium.users.models import User


def get_user_by_email(email: str) -> User:
    user = User.objects.filter(email=email).first()
    if user is None:
        raise UserDoesNotExists
    return user


def create_user(email: str, first_name: str, last_name: str, password: str) -> User:
    user = User.objects.create(email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.save()
    return user


def check_user_exists(email: str) -> bool:
    return User.objects.filter(email=email).exists()


def change_user_password(user: User, current_password: str, new_password: str) -> None:
    if not user.check_password(current_password):
        raise ChangePasswordException
    user.set_password(new_password)
    user.save()


def update_user(user_email: str, first_name: str, last_name: str) -> int:
    users = User.objects.filter(email=user_email)
    if not users.exists():
        raise UserDoesNotExists
    if not users.count() == 1:
        raise MultipleUsersReturned
    return users.update(first_name=first_name, last_name=last_name)
