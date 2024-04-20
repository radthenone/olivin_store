from abc import ABC, abstractmethod


class IClient(ABC):
    @abstractmethod
    def connect(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def disconnect(self, *args, **kwargs) -> None:
        pass
