from repositorium.learning_resources.models import Category
from repositorium.learning_resources.exceptions import (
    CategoryAlreadyExists,
    CategoryDoesNotExists,
)


def category_exists(name: str) -> bool:
    return Category.objects.filter(name=name).exists()


def create_category(name: str) -> Category:
    if not category_exists:
        category = Category.objects.create(name=name)
        return category
    else:
        raise CategoryAlreadyExists


def get_category(name: str) -> Category:
    category = Category.objects.filter(name=name).first()
    if category is None:
        raise CategoryDoesNotExists
    return category
