import io
import mimetypes
import pathlib
import posixpath
from mimetypes import guess_type
from typing import BinaryIO, Optional, TypeVar, Union
from uuid import UUID

from django.conf import settings
from ninja import UploadedFile

ObjectType = TypeVar("ObjectType", bound=Union[UUID, str, int])


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


def path_file(
    filename: str,
    folder: str,
    object_key: Optional[ObjectType] = None,
) -> BinaryIO:
    full_object_path = f"{folder}/{filename}"
    if object_key:
        full_object_path = f"{folder}/{object_key}/{filename}"

    file_path = settings.BASE_DIR / full_object_path
    return open(file_path, "rb")


def upload_file(
    filename: str,
    file: UploadedFile | BinaryIO,
    content_type: Optional[str] = None,
) -> UploadedFile:
    file_io = io.BytesIO()
    if isinstance(file, UploadedFile):
        contents = file.file.read()
        file_io.write(contents)
        file_size = len(contents)
    else:
        contents = file.read()
        file_io.write(contents)
        file_io.seek(0, io.SEEK_END)
        file_size = file_io.tell()
        file_io.seek(0)

    filename = clean_name(filename)
    if content_type:
        filename = filename.split(".")[0] + "." + content_type.split("/")[1]

    return UploadedFile(
        file=file_io,
        name=filename,
        content_type=content_type or mimetypes.guess_type(filename)[0],
        size=file_size,
    )


def get_file_size(file: UploadedFile) -> int:
    return file.size


def get_content_type(file: UploadedFile) -> str:
    return guess_type(file.name)[0]


def get_file_io(file: UploadedFile) -> BinaryIO:
    file_io = io.BytesIO()
    file_io.write(file.file.read())
    file_io.seek(0)
    return file_io
