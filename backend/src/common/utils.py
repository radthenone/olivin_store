import json
from typing import Any, Callable

from dependency_injector import providers
from ninja import Schema
from pydantic import BaseModel


class Depends:
    def __init__(self, fn: Callable = None):
        self.fn = fn
        self.provider = providers.Callable(fn)

    def __call__(self, *args, **kwargs):
        return self.provider(*args, **kwargs)

    def __repr__(self):
        return DependsModel(depends=self).to_json()


class DependsModel(BaseModel):
    depends: Any

    def to_json(self) -> str:
        function_name = self.depends.fn.__name__
        result = {function_name: self.depends()}
        return json.dumps(result)
