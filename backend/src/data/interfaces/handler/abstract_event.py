from abc import ABC, abstractmethod
from typing import Optional, Union


class IEventHandler(ABC):
    @abstractmethod
    def pub(self, event_name: str, event_data: str | dict) -> None:
        pass

    @abstractmethod
    def sub(self, subs: Union[list[str], str]) -> None:
        pass

    @abstractmethod
    def get(self, event_name: str) -> Optional[dict]:
        pass
