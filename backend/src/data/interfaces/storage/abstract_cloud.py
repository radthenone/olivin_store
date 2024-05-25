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
    def upload_template(self, template_name):
        pass

    @abstractmethod
    def get_template(self, template_name):
        pass

    @abstractmethod
    def upload_file(
        self,
        object_key: ObjectType,
        file: UploadedFile,
        new_filename: Optional[str] = None,
        new_content_type: Optional[str] = None,
    ) -> bool:
        pass

    @abstractmethod
    def get_file(
        self,
        object_key: ObjectType,
    ) -> str:
        pass

    @abstractmethod
    def delete_file(
        self,
        object_key: ObjectType,
    ) -> bool:
        pass

    def is_object_exist(
        self,
        object_key: ObjectType,
        path: Optional[str] = None,
    ) -> bool:
        pass
