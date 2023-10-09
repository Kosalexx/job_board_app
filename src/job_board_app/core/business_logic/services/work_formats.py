"""
Services and business logic for working with data associated with WorkFormat entity in the database.
"""

from core.models import WorkFormat


def get_work_formats() -> list[tuple[str, str]]:
    """Gets work formats info from DB to EditProfileForm."""

    formats = [(value.name, value.name) for value in WorkFormat.objects.all()]
    return formats
