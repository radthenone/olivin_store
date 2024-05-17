import logging
import os
import time
from typing import Optional

import boto3
from botocore.client import BaseClient, ClientError
from django.conf import settings

from src.data.interfaces.client.abstract_client import IClient

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "src.core.settings.dev"),
)

logger = logging.getLogger(__name__)


class AmazonClient(IClient):
    amazon_s3: Optional[BaseClient] = None

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        region_name: str = "eu-central-1",
        *args,
        **kwargs,
    ) -> None:
        self.amazon_s3: Optional[BaseClient] = self.connect(
            access_key=access_key,
            secret_key=secret_key,
            region_name=region_name,
            *args,
            **kwargs,
        )
        self.bucket_name = settings.BUCKET_NAME
        self._load_basic_buckets()

    def _load_basic_buckets(self) -> None:
        if not self.amazon_s3.list_buckets()["Buckets"]:
            self.amazon_s3.create_bucket(
                Bucket=self.bucket_name,
                CreateBucketConfiguration={
                    "LocationConstraint": settings.AWS_REGION_NAME
                },
            )

    def connect(
        self,
        access_key: str,
        secret_key: str,
        region_name: str,
        *args,
        **kwargs,
    ) -> BaseClient:
        try:
            session = boto3.session.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region_name,
            )

            self.amazon_s3 = session.client("s3")
            return self.amazon_s3

        except ClientError as error:
            logger.error(error)

    def disconnect(self, **kwargs) -> None:
        self.amazon_s3.close()
