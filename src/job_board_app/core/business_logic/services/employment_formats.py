"""
Services and business logic for working with data associated with EmploymentFormat entity in the database.
"""

from core.models import EmploymentFormat


def get_employment_formats() -> list[tuple[str, str]]:
    """Gets employment formats info from DB to EditProfileForm."""

    formats = [(value.name, value.name) for value in EmploymentFormat.objects.all()]
    return formats
