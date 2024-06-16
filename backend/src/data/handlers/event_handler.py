import importlib
import inspect
import logging
import queue
import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor
from typing import TYPE_CHECKING, Callable, Optional, Union

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
        self.executor = ThreadPoolExecutor()

    @staticmethod
    def start_handlers() -> None:
        if bool(settings.WORKING_HANDLERS or settings.WORKING_HANDLERS != []):
            for event_class in settings.WORKING_HANDLERS:
                module_path, class_name, service_name, method_name = event_class.rsplit(
                    sep=".", maxsplit=3
                )
                cls = getattr(importlib.import_module(module_path), class_name)
                method = getattr(cls.service, method_name)
                if method.__name__.startswith("handle"):
                    event_name = method.__name__.replace("handle_", "")
                    logger.info(
                        "Starting %s for event: %s", method.__name__, event_name
                    )
                    threading.Thread(target=method).start()

    def publish(self, event_name: str, event_data: str | dict) -> None:
        logger.info("Publishing event: %s with data: %s", event_name, event_data)
        threading.Thread(
            target=self.manager.publish,
            args=(event_name, event_data),
        ).start()

    def subscribe(self, event_name: str) -> Optional[dict]:
        self.manager.subscribe(event_name=event_name)
        while True:
            time.sleep(1)
            event_data = self.manager.receive_event(
                event_name=event_name,
            )
            if event_data:
                logger.info("Received event: %s with data: %s", event_name, event_data)
                return event_data
