from typing import TypeVar, Union

from django.conf import settings

from src.data.clients import AmazonClient, MinioClient
from src.data.storages import AmazonS3Storage, MinioStorage

StorageType = TypeVar("StorageType", bound=Union["MinioStorage", "AmazonS3Storage"])


def get_storage():
    if settings.USE_S3_AMAZON:
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
