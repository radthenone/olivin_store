import json
import logging
import mimetypes
from typing import Optional, TypeVar, Union
from uuid import UUID

from django.conf import settings
from django.core.files.storage import Storage
from minio.datatypes import Bucket
from minio.error import S3Error
from minio.helpers import ObjectWriteResult
from ninja.files import UploadedFile
from ninja_extra.exceptions import APIException

from src.data.clients import MinioClient
from src.data.interfaces import ICloudStorage
from src.data.utils import (
    change_file_content_type,
    change_file_name,
    clean_name,
    get_content_type,
    get_file_io,
    get_file_size,
)

logger = logging.getLogger(__name__)

ObjectType = TypeVar("ObjectType", bound=Union[UUID, str, int])


class MinioStorage(ICloudStorage, Storage):
    def __init__(self, client: MinioClient) -> None:
        self.client = client.minio
        self.bucket_name = client.bucket_name
        self.static = client.static
        self.region = client.region
        self._bucket = None
        self.basic_content_type = "application/octet-stream"
        self.add_prefix_policy(path=["static/*", "media/*"])

    @property
    def bucket(self) -> Bucket:
        if not self._bucket:
            self._bucket: Bucket = self.client.make_bucket(
                bucket_name=self.bucket_name,
                location=self.region,
                object_lock=False,
            )
        return self._bucket

    def add_prefix_policy(self, path: list[str] = None):
        if path is None:
            path = [""]
        prefix_resources = [f"arn:aws:s3:::{self.bucket_name}/{p}*" for p in path]

        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": ["*"]},
                    "Action": "s3:GetBucketLocation",
                    "Resource": f"arn:aws:s3:::{self.bucket_name}",
                },
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": ["*"]},
                    "Action": "s3:GetObject",
                    "Resource": prefix_resources,
                },
            ],
        }
        policy_json = json.dumps(policy)
        self.client.set_bucket_policy(bucket_name=self.bucket_name, policy=policy_json)

    def get_full_object_key(self, name, path=None) -> str:
        name = clean_name(name)
        if path is None:
            return name
        return f"{path}/{name}"

    def upload_file(
        self,
        object_key: ObjectType,
        file: UploadedFile,
        new_filename: Optional[str] = None,
        new_content_type: Optional[str] = None,
    ) -> Optional[ObjectWriteResult]:
        content_type = get_content_type(file=file) or self.basic_content_type
        if new_filename:
            file = change_file_name(file=file, new_name=new_filename)
        if new_content_type:
            content_type = change_file_content_type(
                file=file, new_content_type=new_content_type
            )
        length = get_file_size(file=file)
        file_io = get_file_io(file=file)
        try:
            object_name = self.get_available_name(object_key)
            return self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=file_io,
                length=length,
                content_type=content_type,
            )
        except APIException as error:
            logger.error(error)
            return None

    def get_file(
        self,
        object_key: ObjectType,
    ) -> str:
        return self.client.presigned_get_object(self.bucket_name, object_key)

    def delete_file(
        self,
        object_key: ObjectType,
    ) -> bool:
        try:
            self.client.remove_object(
                bucket_name=self.bucket_name,
                object_name=object_key,
            )
            return True
        except APIException as error:
            logger.error(error)
            return False

    # django storage static files

    def exists(self, name: str) -> bool:
        full_object_key = self.get_full_object_key(name, path=self.static)
        try:
            self.client.stat_object(self.bucket_name, full_object_key)
            return True
        except S3Error as error:
            if error.code == "NoSuchKey":
                return False
            logger.error(error)
            return False

    def save(self, name, content, max_length=None):
        name = self.get_available_name(name, max_length=max_length)
        content_type = get_content_type(content)
        content_size = get_file_size(file=content)

        full_object_key = self.get_full_object_key(name, path=self.static)
        try:
            self.client.put_object(
                self.bucket_name,
                full_object_key,
                content,
                content_size,
                content_type=content_type,
            )
        except S3Error as error:
            logger.error(error)
            raise

        return name

    def delete(self, name):
        full_object_key = self.get_full_object_key(name, path=self.static)
        try:
            self.client.remove_object(self.bucket_name, full_object_key)
        except S3Error as error:
            logger.error(error)
            raise

    def url(self, name):
        base_url = settings.STATIC_URL
        if base_url:
            return f"{base_url}{name}"
        else:
            full_object_key = self.get_full_object_key(name, path=self.static)
            return self.client.presigned_get_object(self.bucket_name, full_object_key)

    def size(self, name):
        full_object_key = self.get_full_object_key(name, path=self.static)
        try:
            stat = self.client.stat_object(self.bucket_name, full_object_key)
            return stat.size
        except S3Error as error:
            logger.error(error)
            raise

    def listdir(self, path):
        full_object_key = self.get_full_object_key(path, path=self.static)
        try:
            objects = self.client.list_objects(
                self.bucket_name, prefix=full_object_key, recursive=False
            )
            directories, files = [], []
            for obj in objects:
                if obj.is_dir:
                    directories.append(obj.object_name)
                else:
                    files.append(obj.object_name)
            return directories, files
        except S3Error as error:
            logger.error(error)
            raise
