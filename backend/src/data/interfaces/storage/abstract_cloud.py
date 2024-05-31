from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Union
from uuid import UUID

from ninja.files import UploadedFile

ObjectType = TypeVar("ObjectType", bound=Union[UUID, str, int])


class ICloudStorage(ABC):
    @abstractmethod
    def get_full_object_key(
        self,
        name: ObjectType,
        path: str,
    ) -> str:
        pass

    @abstractmethod
    def add_prefix_policy(self, path: list[str] = None):
        pass

    @abstractmethod
    def get_object_key(
        self,
        filename: str,
        folder: str,
        object_key: Optional[ObjectType] = None,
    ) -> str:
        pass

    @abstractmethod
    def upload_file_from_path(
        self,
        filename: str,
        folder: str,
        object_key: Optional[ObjectType] = None,
        content_type: Optional[str] = None,
    ) -> bool:
        pass

    @abstractmethod
    def upload_file_from_url(
        self,
        filename: str,
        folder: str,
        file: UploadedFile,
        object_key: Optional[ObjectType] = None,
        content_type: Optional[str] = None,
    ) -> bool:
        pass

    @abstractmethod
    def get_file(
        self,
        filename: str,
        folder: Optional[str] = None,
        object_key: Optional[ObjectType] = None,
    ) -> Optional[str]:
        pass

    @abstractmethod
    def delete_file(
        self,
        filename: str,
        folder: Optional[str] = None,
        object_key: Optional[ObjectType] = None,
    ) -> bool:
        pass

    def is_object_exist(
        self,
        full_object_key: ObjectType,
    ) -> bool:
        pass
