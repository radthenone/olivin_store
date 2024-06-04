import logging
import threading
from typing import TYPE_CHECKING, Callable, List, Optional, Union

from django.conf import settings

from src.data.interfaces import IEventHandler

if TYPE_CHECKING:
    from src.data.interfaces import IEventManager

logger = logging.getLogger(__name__)


class EventHandler(IEventHandler):
    """
    Class for handling events.

    Attributes:
        manager (EventManager): Event manager.

    Methods:
        pub(event_name: str, event_data: dict)
        sub(subs: Union[list[str], str])
        get()

    Usage:
        event_handler = EventHandler(event_manager)
        event_handler.pub("test_event", {"key": "value"})
        event_handler.sub("test_event")
        event_handler.get()
    """

    def __init__(
        self,
        manager: "IEventManager",
    ):
        self.manager = manager
        self.methods = None

    @staticmethod
    def start_event_listener() -> None:
        method = "event_listener"
        if bool(settings.WORKING_EVENTS or settings.WORKING_EVENTS != []):
            for class_path in settings.WORKING_EVENTS:
                module_name, class_name = class_path.rsplit(".", 1)
                module = __import__(module_name, fromlist=[class_name])
                class_instance = getattr(module, class_name)
                if hasattr(class_instance, method):
                    method = getattr(class_instance, method)
                    listener_thread = threading.Thread(
                        target=method, args=[class_instance]
                    )
                    listener_thread.daemon = True
                    listener_thread.start()

    def pub(self, event_name: str, event_data: dict) -> None:
        self.manager.publish(event_name, event_data)

    def sub(self, subs: Union[list[str], str]) -> None:
        if isinstance(subs, str):
            subs = [subs]
        self.manager.subscribe(event_list=subs)

    def get(self) -> Optional[dict]:
        return self.manager.receive_event()
