import json
import logging
from typing import Any, Callable, TypeVar

from django.core.cache import cache
from django.http import JsonResponse
from injector import Binder, Injector, ProviderOf, inject
from ninja import Router, Schema
from ninja.types import DictStrAny
from pydantic import ConfigDict, Extra, model_validator

from src.common.tasks import divide

T = TypeVar("T")


class DependsModel(Schema):
    def __new__(cls, depends: T, provider: ProviderOf[T]):
        cls.depends = depends
        cls.provider = provider
        return super().__new__(cls)

    def dict(self) -> DictStrAny:
        result = {str(self.depends.__name__): self.provider.get()}
        return result

    model_config = ConfigDict(
        from_attributes=False,
        extra="allow",
    )

    @model_validator(mode="wrap")
    @classmethod
    def _run_root_validator(
        cls,
        values: Any,
        handler,
        info,
        *args,
        **kwargs,
    ) -> Any:
        return handler(values)


class Depends:
    @inject
    def __init__(self, depends: T):
        self._depends = depends
        self.type = type(depends)
        self.injector = Injector([self.configure])
        self._provider = self.injector.get(ProviderOf[self.type])

    def configure(self, binder: Binder):
        binder.bind(self.type, to=self._depends)

    def __repr__(self):
        return json.dumps(
            DependsModel(depends=self._depends, provider=self._provider).dict()
        )


logger = logging.getLogger(__name__)

router = Router()


def provide_int():
    return 123


@router.get("/hello")
def hello(request, x: DictStrAny = Depends(provide_int)):
    logger.info(msg="Hello World", extra={**x})
    return JsonResponse({"message": "Hello World"})


@router.post("/ping")
def ping(request):
    cache.set("ping", "pong", 5)
    return JsonResponse({"message": "make ping"})


@router.get("/pong")
def pong(request):
    message = cache.get("ping")
    return JsonResponse({"message": message})


@router.get("/task")
def task(request):
    result = divide.delay(5, 2)
    return JsonResponse(
        {
            "task_id": result.task_id,
            "message": result.get(),
        }
    )
