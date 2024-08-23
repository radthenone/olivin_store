import importlib
import logging
import threading
from typing import TYPE_CHECKING, Optional

from django.conf import settings

from src.data.interfaces import IEventHandler

if TYPE_CHECKING:
    from src.data.interfaces import IEventManager

logger = logging.getLogger(__name__)


class EventHandler(IEventHandler):
    def __init__(
        self,
        manager: "IEventManager",
    ):
        self.manager = manager

    def start_handlers(self) -> None:
        if bool(settings.WORKING_HANDLERS or settings.WORKING_HANDLERS != []):
            for event_class in settings.WORKING_HANDLERS:
                module_path, class_name, service_name, method_name = event_class.rsplit(
                    sep=".", maxsplit=3
                )
                controller = getattr(importlib.import_module(module_path), class_name)
                services_methods = [
                    getattr(controller, x)
                    for x in dir(controller)
                    if "service" in x
                    and hasattr(getattr(controller, x), method_name)
                    and callable(getattr(getattr(controller, x), method_name))
                ]
                for service in services_methods:
                    method = getattr(service, method_name)

                    if method.__name__.startswith("handle"):
                        event_name = method.__name__.replace("handle_", "")
                        logger.info(
                            "Starting [green]%s[/] for event: [yellow]%s[/] in service: [bold red blink]%s[/]",
                            method.__name__,
                            event_name,
                            service.__class__.__name__,
                            extra={"markup": True},
                        )
                        threading.Thread(target=method).start()

    def start_subscribers(self) -> None:
        if bool(settings.WORKING_SUBSCRIBERS or settings.WORKING_SUBSCRIBERS != []):
            for subscriber in settings.WORKING_SUBSCRIBERS:
                (
                    logger.info(
                        "Starting subscriber event: [yellow]%s[/]",
                        subscriber,
                        extra={"markup": True},
                    ),
                )
                threading.Thread(target=self.subscribe, args=(subscriber,)).start()
        else:
            logger.info(
                "start_subscribers: No subscribers found",
                extra={"markup": True},
            )

    def publish(self, event_name: str, event_data: str | dict) -> None:
        self.manager.publish(event_name=event_name, event_data=event_data)

    def subscribe(
        self,
        event_name: str,
    ) -> None:
        self.manager.subscribe(event_name=event_name)

    def _process_event(
        self,
        event_name: str,
        timeout: Optional[None | float] = None,
    ) -> Optional[dict]:
        try:
            # Receive event data using the manager
            event_data = self.manager.receive(
                event_name=event_name,
                timeout=timeout,
            )

            # Check if the event data is valid and return it
            if event_data and isinstance(event_data, dict):
                return event_data
            else:
                logger.warning("Received invalid event data for event: %s", event_name)
                return None
        except Exception as e:
            logger.error("Error processing event %s: %s", event_name, str(e))
            return None

    def receive(
        self,
        event_name: str,
        timeout: Optional[None | float] = None,
        with_subscription: bool = False,
    ) -> Optional[dict]:
        if with_subscription:
            self.subscribe(event_name=event_name)

        if not (self.manager.is_subscribed(event_name=event_name) or with_subscription):
            logger.info("Event %s is not subscribed", event_name)
            return None

        if timeout is None:
            return self._process_event(event_name=event_name)
        else:
            return self._process_event(event_name=event_name, timeout=timeout)

    def unsubscribe(
        self,
        event_name: str,
    ) -> None:
        logger.info("Unsubscribing from event: %s", event_name)
        self.manager.unsubscribe(event_name=event_name)
