import json
import logging
import time
from typing import Optional

from src.data.clients import RedisClient

logger = logging.getLogger(__name__)


class EventManager:
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
        event_data: dict,
    ):
        json_data = json.dumps(event_data)
        self.redis.publish(
            channel=event_name,
            message=json_data,
        )
        logger.info("Event %s published", event_name)

    def subscribe(
        self,
        event_name: Optional[str] = None,
        event_list: Optional[list[str]] = None,
    ):
        if not event_name and not event_list:
            raise ValueError("Either 'event_name' or 'event_list' must be provided")

        if event_name:
            self._validate_event_name(event_name)
            self.pubsub.subscribe(event_name)
            logger.info("Subscribed to event %s", event_name)
        else:
            self._validate_event_list(event_list)
            self.pubsub.subscribe(*event_list)
            logger.info("Subscribed to events %s", event_list)

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
            logger.info("Unsubscribed from event %s", event_name)
        else:
            self._validate_event_list(event_list)
            self.pubsub.unsubscribe(*event_list)
            logger.info("Unsubscribed from events %s", event_list)

    def receive_event(self) -> Optional[dict]:
        while message := self.pubsub.get_message():
            if message and message["type"] == "message":
                data = json.loads(message["data"])
                logger.info("Event received: %s", data)
                return data
            time.sleep(0.2)
        return None
