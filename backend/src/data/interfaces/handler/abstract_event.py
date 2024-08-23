from abc import ABC, abstractmethod
from typing import Callable, Optional, Union


class IEventHandler(ABC):
    @abstractmethod
    def start_handlers(self) -> None:
        pass

    @abstractmethod
    def start_subscribers(self) -> None:
        pass

    @abstractmethod
    def publish(self, event_name: str, event_data: Union[str, dict]) -> None:
        pass

    @abstractmethod
    def subscribe(self, event_name: str) -> None:
        pass

    @abstractmethod
    def receive(
        self,
        event_name: str,
        timeout: Optional[None | float] = None,
        with_subscription: bool = False,
    ) -> Optional[dict]:
        pass
