import json
import logging
import mimetypes
from typing import Optional, TypeVar, Union
from uuid import UUID

from botocore.exceptions import ClientError
from django.conf import settings
from django.core.files.storage import Storage
from ninja import UploadedFile
from ninja_extra.exceptions import APIException

from src.data.clients import AmazonClient
from src.data.interfaces import ICloudStorage
from src.data.utils import (
    clean_name,
    path_file,
    upload_file,
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
            file = path_file(
                filename=filename,
                folder=folder,
                object_key=object_key,
            )
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
        full_object_key = self.get_object_key(
            filename=uploaded_file.name,
            folder=folder,
            object_key=object_key,
        )

        if not self.is_object_exist(full_object_key):
            try:
                self.client.put_object(
                    Bucket=self.bucket_name,
                    Key=full_object_key,
                    Body=uploaded_file,
                    ContentLength=uploaded_file.size,
                    ContentType=uploaded_file.content_type,
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
                    self.bucket.put_object(
                        Key=full_object_key,
                        Body=uploaded_file,
                        ContentLength=uploaded_file.size,
                        ContentType=uploaded_file.content_type,
                    )
                    return True
                except APIException as error:
                    logger.error(f"Failed to upload file {file.name}: {error}")
                    return False
                except Exception as error:
                    logger.error(f"An unexpected error occurred: {error}")
                    return False
        else:
            logger.info("File already exists in the bucket.")
            return False
        return False

    def get_file(
        self,
        filename: str,
        folder: Optional[str] = None,
        object_key: Optional[ObjectType] = None,
    ) -> Optional[str]:
        full_object_path = self.get_object_key(
            filename=filename,
            folder=folder,
            object_key=object_key,
        )
        try:
            response = self.client.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": full_object_path,
                },
            )
            return response
        except self.client.exceptions.NoSuchKey:
            logger.error(f"File {full_object_path} not found in S3")
            return None
        except Exception as error:
            logger.error(f"Error retrieving file {full_object_path} from S3: {error}")
            return None

    def delete_file(
        self,
        filename: str,
        folder: Optional[str] = None,
        object_key: Optional[ObjectType] = None,
    ) -> bool:
        full_object_path = self.get_object_key(
            filename=filename,
            folder=folder,
            object_key=object_key,
        )
        try:
            self.bucket.delete_object(
                Key=full_object_path,
            )
            return True
        except APIException as error:
            logger.error(error)
            return False

    def is_object_exist(
        self,
        full_object_key: ObjectType,
    ) -> bool:
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=full_object_key)
            return True
        except ClientError as error:
            if error.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
                return False

    # django storage static files

    def exists(self, name: str) -> bool:
        full_object_key = self.get_full_object_key(name, path=self.static)
        return self.is_object_exist(full_object_key)

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
        full_object_key = self.get_full_object_key(name=path, path=self.static)
        objects = self.bucket.objects.filter(Prefix=full_object_key)
        directories, files = [], []
        for obj in objects:
            if obj.key.endswith("/"):
                directories.append(obj.key)
            else:
                files.append(obj.key)
        return directories, files
