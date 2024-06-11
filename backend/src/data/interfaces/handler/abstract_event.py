from abc import ABC, abstractmethod
from typing import Callable, Optional, Union


class IEventHandler(ABC):
    @abstractmethod
    def subscribe(self, event_name: str) -> Optional[dict]:
        pass

    @abstractmethod
    def publish(self, event_name: str, event_data: Union[str, dict]) -> None:
        pass
