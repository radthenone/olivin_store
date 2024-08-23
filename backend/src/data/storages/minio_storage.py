import json
import logging
import mimetypes
import os
from typing import Optional, TypeVar, Union
from uuid import UUID

from django.conf import settings
from django.core.files.storage import Storage
from minio.datatypes import Bucket
from minio.error import S3Error
from ninja.files import UploadedFile
from ninja_extra.exceptions import APIException

from src.data.clients import MinioClient
from src.data.interfaces import ICloudStorage
from src.data.utils import (
    clean_name,
    get_content_type,
    get_extension,
    get_file_io,
    get_file_size,
    path_file,
    upload_file,
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

    def get_object_key(
        self,
        filename: str,
        folder: str,
        object_key: Optional[ObjectType] = None,
    ) -> str:
        if object_key:
            return f"{folder}/{object_key}/{filename}"

        return f"{folder}/{filename}"

    def upload_file_from_path(
        self,
        filename: str,
        folder: str,
        object_key: Optional[ObjectType] = None,
        content_type: Optional[str] = None,
    ) -> bool:
        uploaded_file = None
        try:
            with path_file(
                filename=filename,
                folder=folder,
                object_key=object_key,
            ) as file:
                uploaded_file = upload_file(
                    filename=filename,
                    file=file,
                    content_type=content_type
                    if content_type
                    else mimetypes.guess_type(file.name)[0],
                )
        except Exception as error:
            logger.error(f"Error opening file {filename}: {error}")
        if not uploaded_file:
            return False

        if not uploaded_file:
            return False
        full_object_key = self.get_object_key(
            filename=uploaded_file.name,
            folder=folder,
            object_key=object_key,
        )

        if not self.is_object_exist(full_object_key):
            try:
                self.client.put_object(
                    bucket_name=self.bucket_name,
                    object_name=full_object_key,
                    data=get_file_io(file=uploaded_file),
                    length=uploaded_file.size,
                    content_type=uploaded_file.content_type,
                )
                logger.info(f"File {full_object_key} uploaded to {self.bucket_name}.")
                return True
            except Exception as error:
                logger.error(f"Error uploading file {full_object_key} to S3: {error}")
                return False

        logger.info("File already exists in the bucket.")
        return False

    def upload_file_from_url(
        self,
        filename: str,
        folder: str,
        file: UploadedFile,
        object_key: Optional[ObjectType] = None,
        content_type: Optional[str] = None,
    ) -> bool:
        uploaded_file = upload_file(
            filename=filename,
            file=file,
            content_type=content_type
            if content_type
            else mimetypes.guess_type(filename)[0],
        )
        full_object_key = self.get_object_key(
            filename=uploaded_file.name,
            folder=folder,
            object_key=object_key,
        )

        if not self.is_object_exist(full_object_key):
            if uploaded_file:
                try:
                    file_io = get_file_io(uploaded_file)
                    file_size = file_io.getbuffer().nbytes
                    self.client.put_object(
                        bucket_name=self.bucket_name,
                        object_name=full_object_key,
                        data=file_io,
                        length=file_size,
                        content_type=uploaded_file.content_type,
                    )
                    return True
                except APIException as error:
                    logger.error(f"Failed to upload file {file.name}: {error}")
                    return False
                except Exception as error:
                    logger.error(f"An unexpected error occurred: {error}")
                    return False

        logger.info("File already exists in the bucket.")
        return False

    def get_file(
        self,
        filename: str,
        folder: Optional[str] = None,
        object_key: Optional[ObjectType] = None,
    ) -> Optional[str]:
        full_object_key = self.get_object_key(
            filename=filename,
            folder=folder,
            object_key=object_key,
        )
        if not self.is_object_exist(full_object_key):
            logger.info("File %s not found in %s.", full_object_key, self.bucket_name)
            return None
        try:
            return self.client.presigned_get_object(self.bucket_name, full_object_key)

        except Exception as error:
            logger.error(error)
            return None

    def delete_file(
        self,
        filename: str,
        folder: Optional[str] = None,
        object_key: Optional[ObjectType] = None,
        content_type: Optional[str] = None,
    ) -> bool:
        full_object_key = self.get_object_key(
            filename=filename,
            folder=folder,
            object_key=object_key,
        )
        ext = get_extension(content_type)
        try:
            self.client.remove_object(
                bucket_name=self.bucket_name,
                object_name=full_object_key + ext,
            )
            if not self.is_object_exist(full_object_key):
                logger.info(f"File {full_object_key} deleted from {self.bucket_name}.")
                return True
        except APIException as error:
            logger.error(error)
            return False

    def is_object_exist(
        self,
        full_object_key: ObjectType,
    ) -> bool:
        try:
            self.client.stat_object(
                bucket_name=self.bucket_name, object_name=full_object_key
            )
            return True
        except S3Error as error:
            if error.code == "NoSuchKey":
                return False
            logger.error(error)
            return False

    # django storage static files

    def exists(self, name: str) -> bool:
        full_object_key = self.get_full_object_key(name, path=self.static)
        return self.is_object_exist(full_object_key)

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
