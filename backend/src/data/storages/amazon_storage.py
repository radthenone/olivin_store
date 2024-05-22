import json
import logging
import mimetypes
from typing import Optional, TypeVar, Union
from uuid import UUID

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.files.storage import Storage
from ninja import UploadedFile
from ninja_extra.exceptions import APIException

from src.data.clients import AmazonClient
from src.data.interfaces import ICloudStorage
from src.data.utils import (
    change_file_content_type,
    change_file_name,
    clean_name,
    get_content_type,
    get_file_io,
    get_file_size,
)

ObjectType = TypeVar("ObjectType", bound=Union[UUID, str, int])

logger = logging.getLogger(__name__)


class AmazonS3Storage(ICloudStorage, Storage):
    def __init__(self, client: AmazonClient) -> None:
        self.client = client.amazon_s3
        self.bucket_name = client.bucket_name
        self.static = client.static
        self._bucket = None
        self.basic_content_type = "application/octet-stream"
        self.resource = client.amazon_s3_resource
        self.add_prefix_policy(path=["static/*", "media/*"])

    @property
    def bucket(self):
        if not self._bucket:
            try:
                self.client.head_bucket(Bucket=self.bucket_name)
            except self.client.exceptions.NoSuchBucket:
                try:
                    self.client.create_bucket(
                        Bucket=self.bucket_name,
                        ACL="bucket-owner-full-control",
                        CreateBucketConfiguration={
                            "LocationConstraint": settings.AWS_REGION_NAME,
                        },
                    )
                except self.client.exceptions.BucketAlreadyOwnedByYou:
                    raise APIException(detail="Bucket already exists")
            self._bucket = self.resource.Bucket(self.bucket_name)
        return self._bucket

    def get_full_object_key(self, name, path=None) -> str:
        name = clean_name(name)
        if path is None:
            return name
        return f"{path}/{name}"

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
                    "Action": "s3:*",
                    "Resource": [
                        f"arn:aws:s3:::{self.bucket_name}",
                        f"arn:aws:s3:::{self.bucket_name}/*",
                    ],
                },
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": ["*"]},
                    "Action": "s3:*",
                    "Resource": prefix_resources,
                },
            ],
        }
        policy_json = json.dumps(policy)
        self.client.put_public_access_block(
            Bucket=self.bucket_name,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": False,
                "BlockPublicPolicy": False,
                "IgnorePublicAcls": False,
                "RestrictPublicBuckets": False,
            },
        )
        self.client.put_bucket_policy(Bucket=self.bucket_name, Policy=policy_json)

    def upload_file(
        self,
        object_key: ObjectType,
        file: UploadedFile,
        new_filename: Optional[str] = None,
        new_content_type: Optional[str] = None,
    ) -> bool:
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
            self.bucket.put_object(
                Key=object_key,
                Body=file_io,
                ContentLength=length,
                ContentType=content_type,
            )
            return True
        except APIException as error:
            logger.error(error)
            return False

    def get_file(self, object_key: ObjectType) -> str:
        return self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": object_key,
            },
        )

    def delete_file(
        self,
        object_key: ObjectType,
    ) -> bool:
        try:
            self.bucket.delete_object(
                Key=object_key,
            )
            return True
        except APIException as error:
            logger.error(error)
            return False

    # django storage static files

    def exists(self, name: str) -> bool:
        full_object_key = self.get_full_object_key(name, path=self.static)
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=full_object_key)
            return True
        except ClientError as error:
            if error.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
                return False

    def save(self, name, content, max_length=None):
        name = self.get_available_name(name, max_length=max_length)
        content_type = mimetypes.guess_type(name)[0] or self.basic_content_type
        content_size = content.size
        content.seek(0)
        full_object_key = self.get_full_object_key(name, path=self.static)
        try:
            self.bucket.put_object(
                Key=full_object_key,
                Body=content,
                ContentLength=content_size,
                ContentType=content_type,
            )
            return full_object_key
        except APIException as error:
            logger.error(error)
            return None

    def delete(self, name):
        full_object_key = self.get_full_object_key(name, path=self.static)
        self.bucket.Object(full_object_key).delete()

    def url(self, name):
        base_url = settings.STATIC_URL
        if base_url:
            return f"{base_url}{name}"
        else:
            full_object_key = self.get_full_object_key(name, path=self.static)
            return self.client.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": full_object_key,
                },
            )

    def size(self, name):
        full_object_key = self.get_full_object_key(name, path=self.static)
        return self.bucket.Object(full_object_key).content_length

    def listdir(self, path):
        full_object_key = self.get_full_object_key(path, path=self.static)
        objects = self.bucket.objects.filter(Prefix=full_object_key)
        directories, files = [], []
        for obj in objects:
            if obj.key.endswith("/"):
                directories.append(obj.key)
            else:
                files.append(obj.key)
        return directories, files
