"""
Services and business logic for working with data associated with Auth_group entity in the database.
"""

from django.contrib.auth.models import Group

USER_TYPE_CHOICES = [(group.name, group.name) for group in Group.objects.all()]


def get_groups() -> list[tuple[str, str]]:
    """Gets groups info from DB to EditProfileForm."""

    groups = [
        ("", ""),
    ] + [(value.name, value.name) for value in Group.objects.all()]
    return groups
