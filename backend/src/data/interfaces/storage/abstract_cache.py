from abc import ABC, abstractmethod


class ICacheStorage(ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def connect(self, *args, **kwargs):
        pass

    @abstractmethod
    def disconnect(self, *args, **kwargs):
        pass
