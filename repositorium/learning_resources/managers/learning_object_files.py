from typing import Optional, Union
from uuid import UUID

from repositorium.learning_resources.models import LearningObject, LearningObjectFile


def upload_learning_object_file():
    pass


def get_learning_object_file_by_uuid(
    file_uuid: Union[str, UUID],
) -> Optional[LearningObjectFile]:
    return LearningObjectFile.objects.filter(uuid=file_uuid).first()
