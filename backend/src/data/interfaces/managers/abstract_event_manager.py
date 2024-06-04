from abc import ABC, abstractmethod
from typing import Optional


class IEventManager(ABC):
    @abstractmethod
    def publish(self, event_name: str, event_data: dict) -> None:
        pass

    @abstractmethod
    def subscribe(self, event_name: str, event_list: list[str]) -> None:
        pass

    @abstractmethod
    def unsubscribe(self, event_name: str, event_list: list[str]) -> None:
        pass

    @abstractmethod
    def receive_event(self) -> Optional[dict]:
        pass
