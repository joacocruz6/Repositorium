from typing import Tuple, Union
from uuid import UUID

from django.db.models import QuerySet

from repositorium.learning_resources.exceptions import (
    CategoryAlreadyExists,
    CategoryDoesNotExists,
)
from repositorium.learning_resources.models import Category


def category_exists(name: str) -> bool:
    return Category.objects.filter(name=name).exists()


def create_category(name: str) -> Category:
    if category_exists(name=name):
        raise CategoryAlreadyExists
    return Category.objects.create(name=name)


def get_category_by_name(name: str) -> Category:
    category = Category.objects.filter(name=name).first()
    if category is None:
        raise CategoryDoesNotExists
    return category


def get_category_by_uuid(uuid: Union[str, UUID]) -> Category:
    category = Category.objects.filter(uuid=uuid).first()
    if category is None:
        raise CategoryDoesNotExists
    return category


def get_or_create_category(name: str) -> Tuple[Category, bool]:
    return Category.objects.get_or_create(name=name)


def get_all_categories() -> QuerySet:
    return Category.objects.all()
