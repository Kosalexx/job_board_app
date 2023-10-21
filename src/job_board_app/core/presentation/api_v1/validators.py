from typing import Any, Callable

from rest_framework.serializers import ValidationError


class ValidateAPIData:
    def __init__(self, validator: Callable) -> None:
        self._validator = validator

    def __call__(self, value: Any) -> Any:
        result = self._validator(value=value)
        if not result.get("status"):
            raise ValidationError(detail=result["message"])

        return value
