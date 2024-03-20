from typing import Callable

import injector
from injector import inject
from pydantic import ConfigDict
from pydantic_core import SchemaSerializer, core_schema

#
# class Depends:
#     @inject
#     def __init__(self, dependency: Callable):
#         self.dependency = dependency
#
#     def configure(self, binder):
#         binder.bind(Callable, self.dependency)


# TODO in progress
class Depends(injector.Module):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, dependency: Callable):
        self.dependency = dependency

    def configure(self, binder):
        binder.bind(Callable, self.dependency)

    @classmethod
    def _validate(cls, value):
        return value

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        _ = source_type
        schema = core_schema.no_info_after_validator_function(
            cls._validate,
            handler(set),
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._validate,
                info_arg=False,
                return_schema=core_schema.set_schema(),
            ),
        )
        cls.__pydantic_serializer__ = SchemaSerializer(schema)
        return schema
