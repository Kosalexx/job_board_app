"""
Custom validators.
"""

from django.core.exceptions import ValidationError
from django.core.files import File


def validate_swear_words_in_company_name(value: str) -> None:
    """Validates company name."""

    if 'fuck' in value.lower():
        raise ValidationError('Company name contains swear words.')


class ValidateMaxTagCount:
    """Validates the number of tags."""

    def __init__(self, max_count: int) -> None:
        self._max_count = max_count

    def __call__(self, value: str) -> None:
        number_of_tags = len(value.split('\r\n'))

        if number_of_tags > self._max_count:
            raise ValidationError(message=f'Max number of tags is {self._max_count}')


class ValidateMaxAreasCount:
    """Validates the number of business areas."""

    def __init__(self, max_count: int) -> None:
        self._max_count = max_count

    def __call__(self, value: str) -> None:
        number_of_areas = len(value.split('\r\n'))

        if number_of_areas > self._max_count:
            raise ValidationError(message=f'Max number of business areas is {self._max_count}')


class ValidateFileExtensions:
    """Validates file extensions."""

    def __init__(self, available_extensions: list[str]) -> None:
        self._available_extensions = available_extensions

    def __call__(self, value: File) -> None:
        file_extensions = value.name.split('.')[-1]
        if file_extensions not in self._available_extensions:
            raise ValidationError(message=f"Accept only {self._available_extensions}.")


class ValidateFileSize:
    """Validates file size."""

    def __init__(self, max_size: int) -> None:
        self._max_size = max_size

    def __call__(self, value: File) -> None:
        file_size = value.size
        if file_size > self._max_size:
            max_size_in_mb = int(self._max_size / 1_000_000)
            raise ValidationError(message=f"Max file size is {max_size_in_mb} MB.")


class ValidateImageExtensions:
    """Validates image extensions."""

    def __init__(self, available_extensions: list[str]) -> None:
        self._available_extensions = available_extensions

    def __call__(self, value: File) -> None:
        image_extensions = value.name.split('.')[-1]
        if image_extensions not in self._available_extensions:
            raise ValidationError(message=f"Accept only {self._available_extensions}.")
