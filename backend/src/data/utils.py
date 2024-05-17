import io
from mimetypes import guess_type
from typing import BinaryIO
from urllib.parse import urlparse
from uuid import UUID

from django.conf import settings
from ninja import UploadedFile


def get_url(name: str) -> str:
    return urlparse(name).geturl()


def get_file_size(file: UploadedFile) -> int:
    return file.size


def get_content_type(file: UploadedFile) -> str:
    return guess_type(file.name)[0]


def get_file_io(file: UploadedFile) -> BinaryIO:
    file_io = io.BytesIO()
    file_io.write(file.file.read())
    file_io.seek(0)
    return file_io
