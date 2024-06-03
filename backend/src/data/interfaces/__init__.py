from src.data.interfaces.client.abstract_client import IClient
from src.data.interfaces.handler.abstract_cache import ICacheHandler
from src.data.interfaces.handler.abstract_file import IFileHandler
from src.data.interfaces.handler.abstract_mail import IRegistrationEmailHandler
from src.data.interfaces.storage.abstract_cache import ICacheStorage
from src.data.interfaces.storage.abstract_cloud import ICloudStorage

__all__ = [
    "IClient",
    "ICacheHandler",
    "IFileHandler",
    "ICacheStorage",
    "ICloudStorage",
    "IRegistrationEmailHandler",
]
