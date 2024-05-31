from logging import getLogger
from typing import Any, TypeVar, Union
from uuid import UUID

from src.data.interfaces import ICloudStorage

logger = getLogger(__name__)
ObjectType = TypeVar("ObjectType", bound=Union[UUID, str, int])


class TemplateHandler:
    def __init__(self, storage: ICloudStorage, folder: str = "templates"):
        self.storage = storage
        self.folder = folder

    def upload_template(self, template_name: str) -> bool:
        return self.storage.upload_file_from_path(
            filename=template_name,
            folder=self.folder,
        )

    def get_template(self, template_name: str) -> Any:
        return self.storage.get_file_from_path(
            filename=template_name,
            folder=self.folder,
        )
