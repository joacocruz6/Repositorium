from django.http import FileResponse
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class FileManagementAPIView(APIView):

    @parser_classes([FileUploadParser])
    def post(self, request: Request, uuid: str, *args, **kwargs) -> Response:
        pass

    def get(self, request: Request, uuid: str, *args, **kwargs) -> FileResponse:
        pass