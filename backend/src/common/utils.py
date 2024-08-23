import csv
import inspect
import os
from itertools import chain
from pathlib import Path
from typing import Any, Callable

from pydantic.main import create_model

from src.core.config import BASE_DIR, SRC_DIR


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


def find_file_in_folder(start_folder, file_name):
    for item in os.listdir(start_folder):
        full_path = os.path.join(start_folder, item)

        if os.path.isdir(full_path):
            relative_path = find_file_in_folder(full_path, file_name)
            if relative_path:
                return os.path.relpath(relative_path, start=start_folder)
        elif os.path.isfile(full_path) and item == file_name:
            return full_path

    return None


def find_file_path_in_project(file_name):
    file_path = find_file_in_folder(SRC_DIR, file_name)

    if file_path:
        file_path = os.path.join(SRC_DIR.name, str(file_path))
        return file_path
    else:
        return None


def pydantic_model(**kwargs: Any) -> Any:
    annotations = {name: (type(value), ...) for name, value in kwargs.items()}
    config = {"arbitrary_types_allowed": True}
    model = create_model("DynamicModel", **annotations, __config__=config)
    return model(**kwargs).model_dump()
