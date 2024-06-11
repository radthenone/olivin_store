import logging

from django.db import transaction
from django.http import HttpRequest, JsonResponse
from ninja.constants import NOT_SET
from ninja_extra import api_controller, route
from ninja_extra.permissions.common import IsAuthenticated

from src.core.interceptors import AuthBearer
from src.core.storage import get_storage
from src.data.handlers import AvatarFileHandler, CacheHandler, EventHandler
from src.data.managers import EventManager
from src.data.storages import RedisStorage
from src.users.repositories import ProfileRepository
from src.users.services import ProfileService

logger = logging.getLogger(__name__)


@api_controller(
    prefix_or_class="/profiles",
    auth=NOT_SET,
    permissions=[],
    tags=["profiles"],
)
class ProfileController:
    repository = ProfileRepository()
    event_handler = EventHandler(manager=EventManager())
    avatar_handler = AvatarFileHandler(storage=get_storage())
    cache_handler = CacheHandler(pool_storage=RedisStorage())

    service = ProfileService(
        repository=repository,
        event_handler=event_handler,
        avatar_handler=avatar_handler,
        cache_handler=cache_handler,
    )
