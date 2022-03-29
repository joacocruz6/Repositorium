from typing import Dict, List, Optional, Text

from repositorium.learning_resources.models import Category, LearningObject, System


def create_learning_object(
    name: str,
    content: Text,
    categories: List[Category],
    created_on: System,
    created_by: "User",
    extra_data: Optional[Dict] = None,
) -> LearningObject:
    learning_object = LearningObject.objects.create(
        name=name,
        content=content,
        created_on=created_on,
        created_by=created_by,
        extra_data=extra_data,
    )
    learning_object.categories.add(categories)
    return learning_object
