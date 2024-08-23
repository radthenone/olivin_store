import asyncio
import json
import logging
import threading
import time
from datetime import timedelta
from queue import Empty, Queue
from threading import current_thread
from typing import Optional

from src.data.clients import RedisClient
from src.data.interfaces import IEventManager

logger = logging.getLogger(__name__)


class EventManager(IEventManager):
    """
    Class for managing events.

    Attributes:
        client (RedisClient): Redis client.
        redis (Redis): Redis instance.
        pubsub (PubSub): Redis PubSub instance.

    Methods:
        publish(event_name: str, event_data: dict)
        subscribe(event_name: Optional[str] = None, event_list: Optional[list[str]] = None)
        unsubscribe(event_name: str, event_list: Optional[list[str]] = None)
        receive_event()

    Usage:
        event_manager = EventManager()
        event_manager.publish("test_event", {"key": "value"})
        event_manager.subscribe("test_event")
        event_manager.unsubscribe("test_event")
    """

    def __init__(self, client: RedisClient = RedisClient()):
        self.client = client
        self.redis = self.client.redis
        self.pubsub = self.redis.pubsub()

    @staticmethod
    def _validate_event_name(event_name: str):
        if not isinstance(event_name, str):
            raise TypeError("'event_name' must be a string")

    @staticmethod
    def _validate_event_list(event_list: list[str]):
        if not isinstance(event_list, list):
            raise TypeError("'event_list' must be a list of event names")
        if not all(isinstance(event, str) for event in event_list):
            raise ValueError("All elements in 'event_list' must be strings")

    def publish(
        self,
        event_name: str,
        event_data: str | dict,
    ):
        if isinstance(event_data, dict):
            event_data = json.dumps(event_data)
        self.redis.publish(
            channel=event_name,
            message=event_data,
        )
        logger.info(
            "[yellow]Publish[/] Event: [red]%s[/] with data: [blue]%s[/]",
            event_name,
            event_data,
            extra={"markup": True},
        )

    def subscribe(
        self,
        event_name: Optional[str] = None,
        event_list: Optional[list[str]] = None,
    ):
        if not event_name and not event_list:
            raise ValueError("Either 'event_name' or 'event_list' must be provided")

        if event_list:
            self._validate_event_list(event_list)
            for event in event_list:
                self.redis.set(name=f"{event}_subscribed", value=json.dumps(True))
                self.pubsub.subscribe(event)
            logger.info(
                "[yellow]Subscribe[/] to events [red]%s[/]",
                event_list,
                extra={"markup": True},
            )
        else:
            self._validate_event_name(event_name)
            self.pubsub.subscribe(event_name)
            self.redis.set(name=f"{event_name}_subscribed", value=json.dumps(True))
            logger.info(
                "[yellow]Subscribe[/] Event: [red]%s[/]",
                event_name,
                extra={"markup": True},
            )

    def unsubscribe(
        self,
        event_name: str,
        event_list: Optional[list[str]] = None,
    ):
        if not event_name and not event_list:
            raise ValueError("Either 'event_name' or 'event_list' must be provided")

        if event_name:
            self._validate_event_name(event_name)
            self.pubsub.unsubscribe(event_name)
            logger.info(
                "[yellow]Unsubscribe[/] Event: [red]%s[/]",
                event_name,
                extra={"markup": True},
            )
        else:
            self._validate_event_list(event_list)
            self.pubsub.unsubscribe(*event_list)
            logger.info(
                "[yellow]Unsubscribed[/] to events [red]%s[/]",
                event_list,
                extra={"markup": True},
            )

    def receive(
        self,
        event_name: str,
        timeout: Optional[None | float] = None,
    ) -> Optional[dict]:
        end_time = time.time() + timeout if timeout else None

        logger.info(
            "Waiting for event: [yellow]%s[/]",
            event_name,
            extra={"markup": True},
        )

        while True:
            message = self.pubsub.get_message(ignore_subscribe_messages=True)

            if not message or not self._is_message(message, event_name):
                if timeout and time.time() >= end_time:
                    return None
                time.sleep(0.1)
                continue

            try:
                event_data = json.loads(message["data"])
                logger.info(
                    "[yellow]Receive[/] Event: [red]%s[/] with data: [blue]%s[/]",
                    event_name,
                    event_data,
                    extra={"markup": True},
                )
                return event_data
            except json.JSONDecodeError:
                logger.warning(
                    "Failed to decode JSON data for event: [red]%s[/]",
                    event_name,
                    extra={"markup": True},
                )
                return None

    @staticmethod
    def _is_message(msg: Optional[dict], event_name: str) -> bool:
        return msg.get("type") == "message" and msg.get("channel") == event_name

    def is_subscribed(self, event_name: str) -> bool:
        data = self.redis.get(f"{event_name}_subscribed")
        if data is None:
            return False
        else:
            if isinstance(data, str):
                return json.loads(data)
            else:
                return False
