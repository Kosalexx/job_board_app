"""
Custom migration that populate Group table with default values.
"""

from typing import Any

from django.contrib.auth.models import Group, Permission
from django.db import migrations

DEFAULT_VALUES = {"candidate": [], "recruiter": ['add_vacancy', 'add_company']}


def populate_table(apps: Any, schema_editor: Any) -> None:
    """Populates table with default values."""
    for key, value in DEFAULT_VALUES.items():
        group = Group.objects.create(name=key)
        permissions = Permission.objects.filter(codename__in=value)
        group.permissions.set(permissions)


def reverse_table_population(apps: Any, schema_editor: Any) -> None:
    """Reverse table population."""
    for key in DEFAULT_VALUES.keys():
        Group.objects.get(name=key).delete()


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ("core", "0006_populate_country_table"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_table,
            reverse_code=reverse_table_population,
        )
    ]
