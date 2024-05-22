import io
import pathlib
import posixpath
from mimetypes import guess_type
from typing import BinaryIO
from urllib.parse import urlparse
from uuid import UUID

from django.conf import settings
from ninja import UploadedFile


def clean_name(name):
    if isinstance(name, pathlib.PurePath):
        name = str(name)

    # Normalize Windows style paths
    cln_name = posixpath.normpath(name).replace("\\", "/")

    # os.path.normpath() can strip trailing slashes so we implement
    # a workaround here.
    if name.endswith("/") and not cln_name.endswith("/"):
        # Add a trailing slash as it was stripped.
        cln_name += "/"

    # Given an empty string, os.path.normpath() will return ., which we don't want
    if cln_name == ".":
        cln_name = ""

    return cln_name


def get_url(name: str) -> str:
    return urlparse(name).geturl()


def get_file_size(file: UploadedFile) -> int:
    return file.size


def get_content_type(file: UploadedFile) -> str:
    return guess_type(file.name)[0]


def change_file_name(file: UploadedFile, new_name: str) -> UploadedFile:
    file.name = new_name
    return file


def change_file_content_type(
    file: UploadedFile, new_content_type: str = None
) -> UploadedFile:
    if new_content_type is None:
        new_content_type = "image/webp"
    file.content_type = new_content_type
    return file


def get_file_io(file: UploadedFile) -> BinaryIO:
    file_io = io.BytesIO()
    file_io.write(file.file.read())
    file_io.seek(0)
    return file_io
