from django.http import FileResponse
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from repositorium.learning_resources.managers import (
    learning_object_files as learning_object_file_manager,
)


class FileManagementAPIView(APIView):
    @parser_classes([FileUploadParser])
    def post(self, request: Request, uuid: str, *args, **kwargs) -> Response:
        pass

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
