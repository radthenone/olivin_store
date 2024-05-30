from typing import Optional, Union

from src.data.managers import EventManager


class EventHandler:
    """
    Class for handling events.

    Attributes:
        manager (EventManager): Event manager.

    Methods:
        pub(event_name: str, event_data: dict)
        sub(subs: Union[list[str], str])
        get()

    Usage:
        event_handler = EventHandler(event_manager)
        event_handler.pub("test_event", {"key": "value"})
        event_handler.sub("test_event")
        event_handler.get()
    """

    def __init__(self, manager: EventManager):
        self.manager = manager

    def pub(self, event_name: str, event_data: dict) -> None:
        self.manager.publish(event_name, event_data)

    def sub(self, subs: Union[list[str], str]) -> None:
        if isinstance(subs, str):
            subs = [subs]
        self.manager.subscribe(event_list=subs)

    def get(self) -> Optional[dict]:
        return self.manager.receive_event()
