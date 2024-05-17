import logging
from typing import TypeVar, Union
from uuid import UUID

from ninja import UploadedFile
from ninja_extra.exceptions import APIException

from src.data.clients import AmazonClient
from src.data.interfaces import ICloudStorage
from src.data.utils import get_content_type, get_file_io, get_file_size, get_url

ObjectType = TypeVar("ObjectType", bound=Union[UUID, str, int])

logger = logging.getLogger(__name__)


class AmazonS3Storage(ICloudStorage):
    location = ""

    def __init__(self, client: AmazonClient) -> None:
        self.client = client.amazon_s3
        self.bucket_name = client.bucket_name
        self._bucket = None
        self.basic_content_type = "application/octet-stream"

    @property
    def bucket(self):
        if not self._bucket:
            self._bucket = self.client.Bucket(self.bucket_name)
        return self._bucket

    def upload_file(
        self,
        object_key: ObjectType,
        file: UploadedFile,
    ) -> bool:
        content_type = get_content_type(file=file) or self.basic_content_type
        length = get_file_size(file=file)
        file_io = get_file_io(file=file)
        try:
            self.bucket.put_object(
                Key=str(object_key),
                Body=file_io,
                ContentLength=length,
                ContentType=content_type,
            )
            return True
        except APIException as error:
            logger.error(error)
            return False

    def get_file(self, object_key: ObjectType) -> str:
        file = self.bucket.get_object(
            Bucket=self.bucket_name,
            Key=str(object_key),
        )
        return get_url(file.url)

    def delete_file(
        self,
        object_key: ObjectType,
    ) -> bool:
        try:
            self.bucket.delete_object(
                Key=str(object_key),
            )
            return True
        except APIException as error:
            logger.error(error)
            return False
