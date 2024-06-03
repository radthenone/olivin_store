from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, TypeVar, Union
from uuid import UUID

from ninja import UploadedFile

if TYPE_CHECKING:
    from src.data.interfaces import ICloudStorage  # unused import

ICloudStorageType = TypeVar("ICloudStorageType", bound="ICloudStorage")
ObjectType = TypeVar("ObjectType", bound=Union[UUID, str, int])


class IFileHandler(ABC):
    def __init__(self, storage: ICloudStorageType, *args, **kwargs):
        self.storage = storage

    @abstractmethod
    def get_media(
        self,
        filename: str,
        object_key: Optional[ObjectType] = None,
    ) -> str:
        pass

    @abstractmethod
    def upload_media_from_url(
        self,
        filename: str,
        file: UploadedFile,
        object_key: Optional[ObjectType] = None,
        content_type: Optional[str] = None,
    ) -> bool:
        pass

    @abstractmethod
    def upload_media_from_path(
        self,
        filename: str,
        object_key: Optional[ObjectType] = None,
        content_type: Optional[str] = None,
    ) -> bool:
        pass

    @abstractmethod
    def delete_media(
        self,
        filename: str,
        object_key: Optional[ObjectType] = None,
    ) -> bool:
        pass
