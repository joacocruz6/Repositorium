import uuid

from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from repositorium.api.serializers.file_serializers import (
    FileUploadSerializer,
    LearningObjectFileSerializer,
)
from repositorium.learning_resources.exceptions import LearningObjectDoesNotExists
from repositorium.learning_resources.managers import (
    learning_object_files as learning_object_file_manager,
)
from repositorium.learning_resources.managers import (
    learning_objects as learning_object_manager,
)


class FileManagementAPIView(APIView):
    @parser_classes([FileUploadParser])
    def post(self, request: Request, uuid: str, *args, **kwargs) -> Response:
        try:
            learning_object = learning_object_manager.get_learning_object_by_uuid(
                uuid=uuid
            )
            file_uuid = str(uuid.uuid4())
            file_route = f"/files/{learning_object.uuid}/{file_uuid}"
            serializer = FileUploadSerializer(data=request.data)
            if serializer.is_valid():
                learning_object_file = (
                    learning_object_file_manager.upload_learning_object_file(
                        learning_object=learning_object,
                        uuid=file_uuid,
                        file_route=file_route,
                        file_descriptor=serializer.validated_data["file"],
                    )
                )
                file_serializer = LearningObjectFileSerializer(learning_object_file)
                return Response(
                    status=status.HTTP_201_CREATED, data=file_serializer.data
                )
            else:
                data = {"errors": serializer.errors}
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
        except LearningObjectDoesNotExists:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request: Request, uuid: str, *args, **kwargs) -> FileResponse:
        as_attachment = request.query_params.get("as_attachment", False)
        learning_object_file = (
            learning_object_file_manager.get_learning_object_file_by_uuid(
                file_uuid=uuid
            )
        )
        return FileResponse(
            open(learning_object_file.file_route, "rb"), as_attachment=as_attachment
        )