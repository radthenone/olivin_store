from logging import getLogger
from uuid import UUID

from ninja.files import UploadedFile

from src.data.interfaces import ICloudStorage

logger = getLogger(__name__)


class AvatarFileService:
    def __init__(self, storage: ICloudStorage):
        self.storage = storage

    def get_avatar(self, user_id: UUID) -> str:
        return self.storage.get_file(object_key=f"/avatars/{user_id}")

    def upload_avatar(self, user_id: UUID, file: UploadedFile) -> bool:
        return self.storage.upload_file(object_key=f"/avatars/{user_id}", file=file)

    def delete_avatar(self, user_id: UUID) -> bool:
        return self.storage.delete_file(object_key=f"/avatars/{user_id}")


class ProductFileService:
    def __init__(self, storage: ICloudStorage):
        self.storage = storage

    def get_product(self, product_id: UUID) -> str:
        return self.storage.get_file(object_key=f"/products/{product_id}")

    def upload_product(self, product_id: UUID, file: UploadedFile) -> bool:
        return self.storage.upload_file(object_key=f"/products/{product_id}", file=file)

    def delete_product(self, product_id: UUID) -> bool:
        return self.storage.delete_file(object_key=f"/products/{product_id}")
