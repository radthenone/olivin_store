import os
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from django.conf import settings

if TYPE_CHECKING:
    from src.data.interfaces import ICacheHandler, IPhoneHandler
    from src.users.interfaces import IProfileRepository

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "src.core.settings.dev"),
)

# PATHS
SRC_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = SRC_DIR.parent
PROJECT_DIR = BASE_DIR.parent


def get_storage():
    from src.data.clients import AmazonClient, MinioClient
    from src.data.storages import AmazonS3Storage, MinioStorage

    if settings.DEBUG_ON:
        aws_client = AmazonClient(
            access_key=settings.AWS_ACCESS_KEY,
            secret_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION_NAME,
        )
        storage = AmazonS3Storage(client=aws_client)
    else:
        minio_client = MinioClient(
            host=settings.MINIO_HOST,
            port=settings.MINIO_PORT,
            access_key=settings.MINIO_ROOT_USER,
            secret_key=settings.MINIO_ROOT_PASSWORD,
            secure=False,
        )
        storage = MinioStorage(client=minio_client)

    return storage


def get_phone_handler(
    cache: Optional["ICacheHandler"] = None,
    repository: Optional["IProfileRepository"] = None,
) -> "IPhoneHandler":
    from src.data.clients import VonageClient
    from src.data.handlers import FakePhoneHandler, VonagePhoneHandler

    if settings.DEBUG_ON:
        client = VonageClient()
        return VonagePhoneHandler(
            client=client,
            cache=cache,
            repository=repository,
        )
    else:
        return FakePhoneHandler(
            client=None,
            cache=cache,
            repository=repository,
        )
