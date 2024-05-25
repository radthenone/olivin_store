from logging import getLogger
from typing import Optional, TypeVar, Union
from uuid import UUID

from ninja.files import UploadedFile

from src.data.interfaces import ICloudStorage

logger = getLogger(__name__)
ObjectType = TypeVar("ObjectType", bound=Union[UUID, str, int])


class MediaFileHandler:
    def __init__(self, storage: ICloudStorage, folder: str):
        self.storage = storage
        self.folder = folder
        self.set_folder_policy(folder=folder)

    def get_media_key(
        self,
        object_key: ObjectType,
    ):
        return self.storage.get_full_object_key(name=object_key, path=self.folder)

    def set_folder_policy(self, folder):
        self.storage.add_prefix_policy(path=[f"{folder}/*"])

    def get_media(
        self,
        object_key: ObjectType,
    ) -> str:
        object_key = self.get_media_key(object_key=object_key)
        return self.storage.get_file(
            object_key=object_key,
        )

    def upload_media(
        self,
        object_key: ObjectType,
        file: UploadedFile,
        new_filename: Optional[str] = None,
        new_content_type: Optional[str] = None,
    ) -> bool:
        if not self.storage.is_object_exist(object_key=object_key, path=self.folder):
            return self.storage.upload_file(
                object_key=object_key,
                file=file,
                new_filename=new_filename,
                new_content_type=new_content_type,
            )

        return False

    def delete_media(
        self,
        object_key: ObjectType,
    ) -> bool:
        return self.storage.delete_file(
            object_key=object_key,
        )


class AvatarFileHandler(MediaFileHandler):
    def __init__(self, storage: ICloudStorage):
        super().__init__(storage=storage, folder="avatars")

    def get_avatar(self, object_key: ObjectType) -> str:
        return self.get_media(object_key=object_key)

    def upload_avatar(
        self,
        object_key: ObjectType,
        file: UploadedFile,
        new_filename="avatar",
        new_content_type="image/webp",
    ) -> bool:
        return self.upload_media(
            object_key=object_key,
            file=file,
            new_filename=new_filename,
            new_content_type=new_content_type,
        )

    def delete_avatar(self, object_key: ObjectType) -> bool:
        return self.delete_media(object_key=object_key)


class ProductFileHandler(MediaFileHandler):
    def __init__(self, storage: ICloudStorage):
        super().__init__(storage=storage, folder="products")

    def get_product(
        self,
        object_key: ObjectType,
    ) -> str:
        return self.get_media(object_key=object_key)

    def upload_product(
        self,
        object_key: ObjectType,
        file: UploadedFile,
        new_filename="product",
        new_content_type="image/webp",
    ) -> bool:
        return self.upload_media(
            object_key=object_key,
            file=file,
            new_filename=new_filename,
            new_content_type=new_content_type,
        )

    def delete_product(
        self,
        object_key: ObjectType,
    ) -> bool:
        return self.delete_media(object_key=object_key)
