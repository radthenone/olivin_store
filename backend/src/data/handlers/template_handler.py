from logging import getLogger
from typing import Any, TypeVar, Union
from uuid import UUID

from src.data.interfaces import ICloudStorage

logger = getLogger(__name__)
ObjectType = TypeVar("ObjectType", bound=Union[UUID, str, int])


class TemplateHandler:
    def __init__(self, storage: ICloudStorage):
        self.storage = storage
        self.folder = "templates"

    def upload_template(self, template_name: str) -> bool:
        if not self.storage.is_object_exist(template_name, self.folder):
            logger.info(f"Uploading template {template_name}")
            return self.storage.upload_template(template_name)
        logger.info(f"Template {template_name} already exists")
        return False

    def get_template(self, template_name: str) -> Any:
        return self.storage.get_template(template_name)
