from typing import Dict, List, Optional, Text, Union
from uuid import UUID
from venv import create

import arrow
from django.db.models import QuerySet

from repositorium.learning_resources.exceptions import (
    LearningObjectAlreadyExists,
    LearningObjectDoesNotExists,
)
from repositorium.learning_resources.models import Category, LearningObject, System


def is_learning_object_created(title: str) -> bool:
    return LearningObject.objects.filter(title=title).exists()


def create_learning_object(
    title: str,
    content: Text,
    categories: List[Category],
    created_on: System,
    created_by: "User",
    extra_data: Optional[Dict] = None,
) -> LearningObject:
    if is_learning_object_created(title=title):
        raise LearningObjectAlreadyExists
    learning_object = LearningObject.objects.create(
        title=title,
        content=content,
        created_on=created_on,
        created_by=created_by,
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
    original_learning_object: LearningObject, forked_by: "User", forked_on: System
) -> LearningObject:
    title = f"Fork of {original_learning_object.title} by {forked_by.full_name} at {arrow.now().datetime}"
    return create_learning_object(
        title=title,
        content=original_learning_object.content,
        categories=list(original_learning_object.categories.all()),
        created_on=forked_on,
        created_by=forked_by,
        extra_data=original_learning_object.extra_data,
    )
