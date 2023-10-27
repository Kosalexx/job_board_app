"""
Custom validators.
"""
from __future__ import annotations

import re
from typing import TYPE_CHECKING

from typing_extensions import NotRequired, TypedDict

if TYPE_CHECKING:
    from django.core.files import File


class ValidatorResponse(TypedDict):
    status: bool
    message: NotRequired[str]


def validate_swear_words_in_company_name(value: str) -> ValidatorResponse:
    """Validates company name."""
    if "fuck" in value.lower():
        return {"status": False, "message": "Company name contains swear word."}

    return {"status": True}


class ValidateMaxTagCount:
    """Validates the number of tags."""

    def __init__(self, max_count: int) -> None:
        self._max_count = max_count

    def __call__(self, value: str) -> ValidatorResponse:
        number_of_tags = len(re.split("[ \r\n]+", value))

        if number_of_tags > self._max_count:
            return {"status": False, "message": f"Max number of tags is {self._max_count}"}

        return {"status": True}


class ValidateMaxAreasCount:
    """Validates the number of business areas."""

    def __init__(self, max_count: int) -> None:
        self._max_count = max_count

    def __call__(self, value: str) -> ValidatorResponse:
        number_of_areas = len(re.split("[ \r\n]+", value))

        if number_of_areas > self._max_count:
            return {"status": False, "message": f'Max number of business areas is {self._max_count}'}
        return {"status": True}


class ValidateFileExtensions:
    """Validates file extensions."""

    def __init__(self, available_extensions: list[str]) -> None:
        self._available_extensions = available_extensions

    def __call__(self, value: File) -> ValidatorResponse:
        split_file_name = value.name.split(".")
        if len(split_file_name) < 2:
            return {"status": False, "message": f"Accept only {self._available_extensions}"}

        file_extension = split_file_name[-1]

        if file_extension not in self._available_extensions:
            return {"status": False, "message": f"Accept only {self._available_extensions}"}

        return {"status": True}


class ValidateFileSize:
    """Validates file size."""

    def __init__(self, max_size: int) -> None:
        self._max_size = max_size

    def __call__(self, value: File) -> ValidatorResponse:
        if value.size > self._max_size:
            max_size_in_mb = int(self._max_size / 1_000_000)
            return {"status": False, "message": f"Max file size is {max_size_in_mb} MB"}

        return {"status": True}


class ValidateImageExtensions:
    """Validates image extensions."""

    def __init__(self, available_extensions: list[str]) -> None:
        self._available_extensions = available_extensions

    def __call__(self, value: File) -> ValidatorResponse:
        image_extensions = value.name.split('.')[-1]
        if image_extensions not in self._available_extensions:
            return {"status": False, "message": f"Accept only {self._available_extensions}"}

        return {"status": True}
