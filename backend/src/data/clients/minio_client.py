import logging
import os
from typing import Optional

from django.conf import settings
from minio import Minio, S3Error

from src.data.interfaces.client.abstract_client import IClient

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "src.core.settings.dev"),
)


logger = logging.getLogger(__name__)


class MinioClient(IClient):
    minio: Optional[Minio] = None

    def __init__(
        self,
        host: str,
        port: str,
        access_key: str,
        secret_key: str,
        secure: bool = False,
        region_name: str = "eu-central-1",
        *args,
        **kwargs,
    ) -> None:
        self.minio = self.connect(
            host=host,
            port=port,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
            *args,
            **kwargs,
        )
        self._raise_init()
        self.bucket_name = settings.BUCKET_NAME
        self.static = settings.STATIC_PATH
        self.region = region_name
        self._load_basic_buckets()

    @staticmethod
    def _raise_init():
        if not settings.BUCKET_NAME:
            raise ValueError("MINIO: BUCKET_NAME is not set")
        if not settings.STATIC_PATH:
            raise ValueError("MINIO: STATIC_PATH is not set")

    def _load_basic_buckets(self) -> None:
        if not self.minio.bucket_exists(bucket_name=self.bucket_name):
            self.minio.make_bucket(bucket_name=self.bucket_name)

    def connect(
        self,
        host: str,
        port: str,
        access_key: str,
        secret_key: str,
        secure: bool = False,
        *args,
        **kwargs,
    ) -> Minio:
        try:
            if not self.minio:
                endpoint = f"{host}:{port}"
                minio = Minio(
                    endpoint=endpoint,
                    access_key=access_key,
                    secret_key=secret_key,
                    secure=secure,
                )
                self.minio = minio
                return self.minio
        except S3Error as error:
            logger.error(error)

        except Exception as error:
            logger.error(error)

    def disconnect(self, **kwargs) -> None:
        self.minio = None
