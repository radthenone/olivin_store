import logging
from datetime import datetime
from typing import Optional, TypeVar, Union
from uuid import UUID

from minio.datatypes import Bucket
from minio.helpers import ObjectWriteResult
from ninja.files import UploadedFile
from ninja_extra.exceptions import APIException

from src.data.clients import MinioClient
from src.data.interfaces import ICloudStorage
from src.data.utils import get_content_type, get_file_io, get_file_size, get_url

logger = logging.getLogger(__name__)

ObjectType = TypeVar("ObjectType", bound=Union[UUID, str, int])


class MinioStorage(ICloudStorage):
    def __init__(self, client: MinioClient) -> None:
        self.client = client.minio
        self.bucket_name = client.bucket_name
        self._bucket = None
        self.basic_content_type = "application/octet-stream"

    @property
    def bucket(self) -> Bucket:
        if not self._bucket:
            self._bucket = Bucket(
                name=self.bucket_name,
                creation_date=datetime.now(),
            )
        return self._bucket

    def upload_file(
        self,
        object_key: ObjectType,
        file: UploadedFile,
    ) -> Optional[ObjectWriteResult]:
        content_type = get_content_type(file=file) or self.basic_content_type
        length = get_file_size(file=file)
        file_io = get_file_io(file=file)
        try:
            return self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=str(object_key),
                data=file_io,
                length=length,
                content_type=content_type,
            )
        except APIException as error:
            logger.error(error)
            return None

    def get_file(self, object_key: ObjectType) -> str:
        file = self.client.get_object(
            bucket_name=self.bucket_name,
            object_name=str(object_key),
        )
        return get_url(file.url)

    def delete_file(
        self,
        object_key: ObjectType,
    ) -> bool:
        try:
            self.client.remove_object(
                bucket_name=self.bucket_name,
                object_name=str(object_key),
            )
            return True
        except APIException as error:
            logger.error(error)
            return False
