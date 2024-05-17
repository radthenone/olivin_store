from abc import ABC, abstractmethod
from typing import TypeVar, Union
from uuid import UUID

from ninja.files import UploadedFile

ObjectType = TypeVar("ObjectType", bound=Union[UUID, str, int])


class ICloudStorage(ABC):
    @abstractmethod
    def upload_file(
        self,
        object_key: ObjectType,
        file: UploadedFile,
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
