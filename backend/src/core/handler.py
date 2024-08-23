import os
from typing import TYPE_CHECKING, Optional

from django.conf import settings

from src.data.clients import VonageClient
from src.data.handlers import FakePhoneHandler, VonagePhoneHandler

if TYPE_CHECKING:
    from src.data.interfaces import ICacheHandler, IPhoneHandler
    from src.users.interfaces import IProfileRepository


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "src.core.settings.dev"),
)


def get_phone_handler(
    cache: Optional["ICacheHandler"] = None,
    repository: Optional["IProfileRepository"] = None,
) -> "IPhoneHandler":
    if settings.DEBUG_ON:
        client = VonageClient()
        return VonagePhoneHandler(
            client=client,
            cache=cache,
            repository=repository,
        )
    else:
        return FakePhoneHandler(
            client=None,
            cache=cache,
            repository=repository,
        )
