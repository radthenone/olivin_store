from abc import ABC, abstractmethod
from typing import Optional


class IEventManager(ABC):
    @abstractmethod
    def publish(
        self,
        event_name: str,
        event_data: str | dict,
    ) -> None:
        pass

    @abstractmethod
    def subscribe(
        self,
        event_name: Optional[str] = None,
        event_list: Optional[list[str]] = None,
    ) -> None:
        pass

    @abstractmethod
    def unsubscribe(
        self,
        event_name: str,
        event_list: Optional[list[str]] = None,
    ) -> None:
        pass

    @abstractmethod
    def receive(
        self,
        event_name: str,
        timeout: Optional[None | float] = None,
    ) -> Optional[dict]:
        pass

    @abstractmethod
    def is_subscribed(
        self,
        event_name: str,
    ) -> bool:
        pass
