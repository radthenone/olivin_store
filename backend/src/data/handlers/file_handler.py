from logging import getLogger
from typing import Optional, TypeVar, Union
from uuid import UUID

from ninja.files import UploadedFile

from src.data.interfaces import ICloudStorage, IFileHandler

logger = getLogger(__name__)
ObjectType = TypeVar("ObjectType", bound=Union[UUID, str, int])


class MediaFileHandler(IFileHandler):
    def __init__(
        self,
        storage: ICloudStorage,
        folder: str,
        content_type: str = "image/webp",
    ):
        super().__init__(storage=storage)
        self.folder = folder
        self.content_type = content_type
        self._set_folder_policy(folder=folder)

    def _set_folder_policy(self, folder):
        self.storage.add_prefix_policy(path=[f"{folder}/*"])

    def get_media(
        self,
        filename: str,
        object_key: Optional[ObjectType] = None,
    ) -> str:
        return self.storage.get_file(
            filename=filename,
            folder=self.folder,
            object_key=object_key,
        )

    def upload_media_from_url(
        self,
        filename: str,
        file: UploadedFile,
        object_key: Optional[ObjectType] = None,
        content_type: Optional[str] = None,
    ) -> bool:
        try:
            self.storage.upload_file_from_url(
                filename=filename,
                folder=self.folder,
                file=file,
                object_key=object_key,
                content_type=content_type,
            )
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def upload_media_from_path(
        self,
        filename: str,
        object_key: Optional[ObjectType] = None,
        content_type: Optional[str] = None,
    ) -> bool:
        try:
            self.storage.upload_file_from_path(
                filename=filename,
                folder=self.folder,
                object_key=object_key,
                content_type=content_type,
            )
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def delete_media(
        self,
        filename: str,
        object_key: Optional[ObjectType] = None,
    ) -> bool:
        return self.storage.delete_file(
            filename=filename,
            folder=self.folder,
            object_key=object_key,
        )


class AvatarFileHandler(MediaFileHandler):
    def __init__(self, storage: ICloudStorage, filename: str = "avatar"):
        super().__init__(storage=storage, folder="avatars")
        self.filename = filename

    def get_avatar(
        self,
        object_key: Optional[ObjectType] = None,
    ) -> str:
        filename = f"{self.filename}.{self.content_type.split('/')[1]}"
        return self.get_media(
            filename=filename,
            object_key=object_key,
        )

    def upload_avatar(
        self,
        file: UploadedFile,
        object_key: Optional[ObjectType] = None,
    ) -> bool:
        return self.upload_media_from_url(
            filename=self.filename,
            file=file,
            object_key=object_key,
            content_type=self.content_type,
        )

    def delete_avatar(
        self,
        object_key: Optional[ObjectType] = None,
    ) -> bool:
        return self.delete_media(
            filename=self.filename,
            object_key=object_key,
        )


class ProductFileHandler(MediaFileHandler):
    content_type = "image/webp"

    def __init__(self, storage: ICloudStorage, filename: str = "product"):
        super().__init__(storage=storage, folder="products")
        self.filename = filename

    def get_product(
        self,
        object_key: Optional[ObjectType] = None,
    ) -> str:
        filename = f"{self.filename}.{self.content_type.split('/')[1]}"
        return self.get_media(
            filename=filename,
            object_key=object_key,
        )

    def upload_product(
        self,
        file: UploadedFile,
        object_key: Optional[ObjectType] = None,
    ) -> bool:
        return self.upload_media_from_url(
            filename=self.filename,
            file=file,
            object_key=object_key,
            content_type=self.content_type,
        )

    def delete_product(
        self,
        object_key: Optional[ObjectType] = None,
    ) -> bool:
        return self.delete_media(
            filename=self.filename,
            object_key=object_key,
        )


class ImageFileHandler(MediaFileHandler):
    def __init__(self, storage: ICloudStorage):
        super().__init__(storage=storage, folder="media")

    def get_image(
        self,
        filename: str,
        object_key: Optional[ObjectType] = None,
    ) -> str:
        return self.get_media(
            filename=filename,
            object_key=object_key,
        )

    def upload_image(
        self,
        filename: str,
        object_key: Optional[ObjectType] = None,
    ) -> bool:
        return self.upload_media_from_path(
            filename=filename,
            object_key=object_key,
            content_type=self.content_type,
        )

    def delete_image(
        self,
        filename: str,
        object_key: Optional[ObjectType] = None,
    ) -> bool:
        return self.delete_media(
            filename=filename,
            object_key=object_key,
        )
