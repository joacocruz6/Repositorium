from typing import Optional, Union
from uuid import UUID

from django.core.files import File

from repositorium.learning_resources.models import LearningObject, LearningObjectFile


def upload_learning_object_file(
    learning_object: LearningObject,
    uuid: Union[str, UUID],
    file_route: str,
    file_descriptor: File,
) -> LearningObjectFile:
    learning_object_file = LearningObjectFile.objects.create(
        uuid=uuid, file_route=file_route, learning_object=learning_object
    )
    with open(file_route, "wb+") as fd:
        file_descriptor.seek(0)
        for chunk in file_descriptor.chunks():
            fd.write(chunk)
    return learning_object_file


def get_learning_object_file_by_uuid(
    file_uuid: Union[str, UUID],
) -> Optional[LearningObjectFile]:
    return LearningObjectFile.objects.filter(uuid=file_uuid).first()
