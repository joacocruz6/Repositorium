from typing import Union
from uuid import UUID

from repositorium.learning_resources.models import LearningObject, LearningObjectFile


def upload_learning_object_file():
    pass


def get_learning_object_file(
    file_uuid: Union[str, UUID], learning_object_uuid: str
) -> str:
    pass
