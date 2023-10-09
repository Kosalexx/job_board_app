"""
Services and business logic for working with data associated with Levels entity in the database.
"""

from core.models import Level


def get_levels() -> list[tuple[str, str]]:
    """Gets levels info from DB to EditProfileForm."""

    levels = [
        ("", ""),
    ] + [(level.name, level.name) for level in Level.objects.all()]
    return levels
