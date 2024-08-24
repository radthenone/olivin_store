import logging
from typing import TYPE_CHECKING, Optional, cast
from uuid import UUID

from ninja import UploadedFile

from src.common import schemas as common_schemas
from src.data.utils import resize_image
from src.files import errors as file_errors
from src.files import schemas as file_schemas

if TYPE_CHECKING:
    from src.data.handlers import (
        AvatarFileHandler,
    )
    from src.data.interfaces import IFileHandler

logger = logging.getLogger(__name__)


class FileService:
    def __init__(
        self,
        avatar_handler: "IFileHandler",
        size: tuple[int, int] = (150, 150),
    ):
        self.size = size
        self.avatar_handler: "AvatarFileHandler" = cast(
            "AvatarFileHandler", avatar_handler
        )

    def get_avatar_url(self, avatar_key: str) -> Optional[str]:
        avatar_url = self.avatar_handler.get_avatar(object_key=avatar_key)
        if avatar_url:
            return avatar_url.split("?")[0]
        return None

    def _delete_avatar(self, avatar_key: str) -> Optional[bool]:
        return self.avatar_handler.delete_avatar(object_key=avatar_key)

    def _upload_avatar(self, file: UploadedFile, avatar_key: str) -> Optional[bool]:
        resized_file = resize_image(uploaded_file=file, size=self.size)
        return self.avatar_handler.upload_avatar(
            file=resized_file, object_key=avatar_key
        )

    def _exist_avatar(self, avatar_key: str) -> Optional[bool]:
        try:
            if self.get_avatar_url(avatar_key):
                return True
        except FileNotFoundError:
            return False
        except Exception as e:
            logger.exception(e)
            return False

    def get_avatar(self, user_id: UUID) -> Optional[file_schemas.AvatarSchema]:
        avatar_key = str(user_id)
        avatar = self.get_avatar_url(avatar_key)
        if avatar:
            return file_schemas.AvatarSchema(
                avatar=avatar,
            )
        raise file_errors.AvatarNotFound

    def upload_avatar(
        self, file: UploadedFile, user_id: UUID
    ) -> Optional[common_schemas.MessageSchema]:
        avatar_key = str(user_id)
        if self._exist_avatar(avatar_key):
            raise file_errors.AvatarExists
        if self._upload_avatar(file, avatar_key):
            return common_schemas.MessageSchema(message="Avatar uploaded successfully")
        raise file_errors.AvatarUploadFailed

    def update_avatar(
        self, file: UploadedFile, user_id: UUID
    ) -> Optional[common_schemas.MessageSchema]:
        avatar_key = str(user_id)
        if not self._exist_avatar(avatar_key):
            raise file_errors.AvatarNotFound
        if self._delete_avatar(avatar_key) and self._upload_avatar(file, avatar_key):
            return common_schemas.MessageSchema(message="Avatar updated successfully")
        raise file_errors.AvatarUpdateFailed

    def delete_avatar(self, user_id: UUID) -> Optional[common_schemas.MessageSchema]:
        avatar_key = str(user_id)
        if not self._exist_avatar(avatar_key):
            raise file_errors.AvatarNotFound
        if self._delete_avatar(avatar_key):
            return common_schemas.MessageSchema(message="Avatar deleted successfully")
        raise file_errors.AvatarDeleteFailed
