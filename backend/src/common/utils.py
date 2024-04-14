from typing import Any

from pydantic.main import create_model


def pydantic_model(**kwargs: Any) -> Any:
    annotations = {name: (type(value), ...) for name, value in kwargs.items()}
    config = {"arbitrary_types_allowed": True}
    model = create_model("DynamicModel", **annotations, __config__=config)
    return model(**kwargs).model_dump()
