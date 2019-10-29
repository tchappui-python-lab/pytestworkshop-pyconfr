# -*- coding: utf-8 -*-
import mimetypes
from typing import Optional, Any

from django.core.files.storage import DefaultStorage
from django.http import Http404, HttpResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import (
    FileUploadParser, FormParser,
    MultiPartParser
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class StorageWrapper:
    def __init__(self):
        self.storage = DefaultStorage()

    def save(self, filename: str, file_like):
        return self.storage.save(filename, file_like)

    def list(self, ext: str = None):
        _, files = self.storage.listdir("/")
        if ext:
            files = [f for f in files if f.endswith(ext)]
        return files

    def exists(self, filename: str):
        return self.storage.exists(filename)

    def find(self, filename: str) -> Optional[str]:
        for file_ in self.list():
            if file_ == filename:
                return file_
        return None

    def write_to(self, filename: str, callback: Any):
        f = self.storage.open(filename)
        callback(f.read())
        f.close()

    def remove(self, filename: str):
        self.storage.delete(filename)


class FilesViewSet(ViewSet):
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    lookup_field = 'filename'
    lookup_value_regex = r'[\w\s.\-_]+'

    def __init__(self, *args, **kwargs):
        self.client = StorageWrapper()
        super().__init__(*args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        return super().finalize_response(request, response, *args, **kwargs)

    def list(self, _):
        ext = self.request.query_params.get('ext', None)
        files = [{'name': filename} for filename in self.client.list(ext=ext)]
        return Response({'results': files})

    def create(self, request):
        files = request.FILES
        common_files = set(files.keys()) & set(self.client.list())
        if common_files:
            raise ValidationError(
                'File with name(s) `{}` already exists.'.format(
                    ','.join(common_files)
                ), code='unique'
            )
        created_files = []
        for filename, in_mem_file in request.FILES.items():
            self.client.save(filename, in_mem_file)
            created_files.append({'name': filename})
        return Response(created_files, status=status.HTTP_201_CREATED)

    def retrieve(self, request, filename=None):
        file_ = self.client.find(filename)
        if not file_:
            raise Http404
        content_type, encoding = mimetypes.guess_type(filename)
        if content_type is None:
            content_type = 'application/octet-stream'
        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = (
            'attachment; filename="{}"'.format(filename)
        )
        self.client.write_to(filename, response.write)
        return response

    def update(self, request, filename=None):
        if not self.client.exists(filename):
            raise Http404

        self.client.remove(filename)
        return Response({'status': 'ok'})

    def destroy(self, request, filename=None):
        if not self.client.exists(filename):
            raise Http404
        self.client.remove(filename)
        return Response({'status': 'ok'}, status=status.HTTP_204_NO_CONTENT)
