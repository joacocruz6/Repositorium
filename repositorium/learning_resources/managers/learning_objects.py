from typing import Dict, List, Optional, Text, Union
from uuid import UUID

from django.db.models import QuerySet

from repositorium.learning_resources.exceptions import (
    LearningObjectAlreadyExists,
    LearningObjectDoesNotExists,
)
from repositorium.learning_resources.models import (
    Category,
    LearningObject,
    LearningObjectUsage,
    System,
)


def is_learning_object_created(title: str) -> bool:
    return LearningObject.objects.filter(title=title).exists()


def create_learning_object(
    title: str,
    content: Text,
    categories: List[Category],
    description: str,
    created_on: System,
    creator_email: str,
    extra_data: Optional[Dict] = None,
) -> LearningObject:
    if is_learning_object_created(title=title):
        raise LearningObjectAlreadyExists
    learning_object = LearningObject.objects.create(
        title=title,
        content=content,
        description=description,
        created_on=created_on,
        creator_email=creator_email,
        extra_data=extra_data,
    )
    learning_object.categories.add(*categories)
    return learning_object


def get_all_learning_objects() -> QuerySet:
    return LearningObject.objects.all()


def get_learning_object_by_uuid(uuid: Union[str, UUID]) -> LearningObject:
    learning_object = LearningObject.objects.filter(uuid=uuid).first()
    if learning_object is None:
        raise LearningObjectDoesNotExists
    return learning_object


def get_learning_object_by_title(title: str) -> LearningObject:
    learning_object = LearningObject.objects.filter(title=title).first()
    if learning_object is None:
        raise LearningObjectDoesNotExists
    return learning_object


def fork_learning_object(
    original_learning_object: LearningObject,
    forked_by: "User",
    forked_on: System,
    title: str,
    content: str,
    description: str,
    categories: List[Category],
) -> LearningObject:
    return create_learning_object(
        title=title,
        content=content,
        categories=categories,
        created_on=forked_on,
        creator_email=forked_by.email,
        description=description,
        extra_data=original_learning_object.extra_data,
    )


def get_learning_objects_by_category_uuids(categories_uuids: List[str]) -> QuerySet:
    return LearningObject.objects.filter(categories__uuid__in=categories_uuids)


def create_learning_object_usage(
    user: "User", learning_object: LearningObject, system_used: System
):
    usage = LearningObjectUsage.objects.create(
        user=user, learning_object=learning_object, used_on=system_used
    )
    return usage


def get_learning_objects_filter_with_title_and_category(
    title: str, category_names: List[str]
):
    learning_objects = get_all_learning_objects()
    if len(title) > 0:
        learning_objects = learning_objects.filter(title__istartswith=title)
    if len(category_names) > 0:
        learning_objects = learning_objects.filter(
            categories__name__in=category_names
        ).distinct()
    return learning_objects.order_by("-created_at")


def get_learning_objects_with_categories(category_names: List[str]) -> QuerySet:
    return LearningObject.objects.filter(categories__name__in=category_names)


def get_user_last_used_learning_object(user_email: str) -> LearningObject:
    learning_object_usage = (
        LearningObjectUsage.objects.filter(user__email=user_email)
        .order_by("-created_at")
        .first()
    )
    if learning_object_usage is None:
        raise LearningObjectDoesNotExists
    return learning_object_usage
