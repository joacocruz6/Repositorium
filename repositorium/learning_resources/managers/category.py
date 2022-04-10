from typing import List, Tuple, Union
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


def get_or_create_categories(category_names: List[str]) -> Tuple[List[Category], bool]:
    already_created_categories = Category.objects.filter(name__in=category_names)
    if already_created_categories.count() != len(category_names):
        created_categories_names = set(
            already_created_categories.values_list("name", flat=True)
        )
        category_names = set(category_names)
        missing_categories = category_names - created_categories_names
        categories_to_create = [Category(name=name) for name in missing_categories]
        Category.objects.bulk_create(categories_to_create)
        return Category.objects.filter(name__in=category_names), True
    else:
        return already_created_categories, False
