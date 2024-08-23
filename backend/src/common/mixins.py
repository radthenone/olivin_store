import datetime
import json
from typing import Any, Optional

from django.db import models


class ModelToDictToJsonMixin:
    def to_dict(
        self,
        include: Optional[list[str]] = None,
        exclude: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        data: dict[str, Any] = {}

        for field in self._meta.fields:  # noqa:
            value = getattr(self, field.name)

            if isinstance(field, models.UUIDField):
                data[field.name] = str(value) if value else None
            elif isinstance(field, (models.DateField, models.DateTimeField)):
                if isinstance(value, (datetime.date, datetime.datetime)):
                    data[field.name] = value.isoformat() if value else None
                else:
                    data[field.name] = value
            elif isinstance(field, models.ForeignKey or models.OneToOneField):
                data[field.name] = str(value.id) if value else None
            elif isinstance(field, models.URLField):
                data[field.name] = value.url if value else None
            elif isinstance(field, models.ManyToManyField):
                data[field.name] = (
                    [str(item.id) for item in value.all()] if value.exists() else []
                )
            else:
                data[field.name] = value

        if exclude:
            data = {k: v for k, v in data.items() if k not in exclude}

        if include:
            data = {k: v for k, v in data.items() if k in include}

        return data

    def to_json(
        self,
        exclude: Optional[list[str]] = None,
        include: Optional[list[str]] = None,
    ) -> str:
        if hasattr(self, "to_dict"):
            try:
                return json.dumps(self.to_dict(exclude=exclude, include=include))
            except TypeError as error:
                raise ValueError(f"Error serializing to JSON: {error}")
        else:
            raise AttributeError("The object does not have a 'to_dict' method.")
