"""
Services and business logic for working with data associated with Country entity in the database.
"""

from core.models import Country


def get_countries() -> list[tuple[str, str]]:
    """Gets countries info from DB to EditProfileForm."""

    countries = [
        ("", ""),
    ] + [(value.name, value.name) for value in Country.objects.all()]
    return countries
