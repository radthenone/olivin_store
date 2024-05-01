from typing import Optional, Union

from src.data.managers import EventManager


class EventHandler:
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
