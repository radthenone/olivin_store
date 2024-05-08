import inspect
from pathlib import Path
from typing import Any, Callable

from pydantic.main import create_model

from src.core.config import BASE_DIR


def get_module_name(file_path: Path, src_dir: Path) -> str:
    relative_path = file_path.relative_to(src_dir)

    module_name = str(relative_path).replace("\\", ".")[:-3]

    return module_name


def get_full_function_path(
    function: Callable[..., Any],
) -> str:
    file_path = Path(inspect.getfile(function))

    function_name = function.__name__

    module_name = get_module_name(file_path=file_path, src_dir=BASE_DIR)

    full_function_path = f"{module_name}.{function_name}"

    return full_function_path


def pydantic_model(**kwargs: Any) -> Any:
    annotations = {name: (type(value), ...) for name, value in kwargs.items()}
    config = {"arbitrary_types_allowed": True}
    model = create_model("DynamicModel", **annotations, __config__=config)
    return model(**kwargs).model_dump()
