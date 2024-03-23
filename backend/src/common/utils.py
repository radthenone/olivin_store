import json
from typing import Any, Callable

from dependency_injector import providers
from ninja import Schema
from pydantic import Extra


class Depends:
    def __init__(self, fn: Callable = None):
        self.fn = fn
        self.provider = providers.Callable(fn)

    def __call__(self, *args, **kwargs):
        return self.provider(*args, **kwargs)

    def __repr__(self):
        return DependsModel(depends=self).to_json()


class DependsModel(Schema):
    depends: Depends

    def __new__(cls, depends: Depends):
        cls.depends = depends
        return super().__new__(cls)

    def to_json(self) -> str:
        function_name = self.depends.fn.__name__
        result = {function_name: self.depends()}
        return json.dumps(result)

    class Config:
        extra = Extra.forbid
