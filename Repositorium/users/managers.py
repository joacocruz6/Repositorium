from typing import Union
from uuid import UUID

from repositorium.users.exceptions import UserDoesNotExists
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
