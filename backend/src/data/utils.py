import io
import logging
import mimetypes
import pathlib
import posixpath
from mimetypes import guess_type
from typing import BinaryIO, Optional, TypeVar, Union
from uuid import UUID

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from ninja import UploadedFile
from PIL import Image

logger = logging.getLogger(__name__)

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


def get_file_io(file: UploadedFile) -> io.BytesIO:
    file.file.seek(0)
    data = file.file.read()
    file_io = io.BytesIO(data)
    file_io.seek(0)
    return file_io


def get_extension(content_type: str, custom_types: dict = None):
    if custom_types is None:
        custom_types = {
            "image/webp": ".webp",
        }

    if content_type in custom_types:
        return custom_types[content_type]

    ext = mimetypes.guess_extension(content_type)

    if ext is None:
        ext = "." + content_type.split("/")[-1]

    return ext


def resize_image(uploaded_file: UploadedFile, size=(200, 200)) -> UploadedFile:
    uploaded_file.file.seek(0)
    original_data = uploaded_file.file.read()

    with Image.open(io.BytesIO(original_data)) as image:
        image.thumbnail(size, Image.Resampling.LANCZOS)

        output = io.BytesIO()
        image.save(output, format=image.format)
        output_data = output.getvalue()
        logger.info("Resized image size: %s", len(output_data))

        content_file = ContentFile(output_data)

        new_file = UploadedFile(
            file=content_file,
            name=uploaded_file.name,
            content_type=uploaded_file.content_type,
            size=len(output_data),
        )

    return new_file
