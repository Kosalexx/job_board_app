from typing import Any, Callable

from django.core.exceptions import ValidationError


class ValidateWebData:
    def __init__(self, validator: Callable) -> None:
        self._validator = validator

    def __call__(self, value: Any) -> None:
        result = self._validator(value=value)

        if not result["status"]:
            raise ValidationError(message=result["message"])
