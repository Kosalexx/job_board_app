"""
Custom migration that populate WorkFormats table with default values.
"""

from typing import Any

from core.models import WorkFormat
from django.db import migrations

DEFAULT_VALUES = ("Remote work", "Office work", "Hybrid", "Full-time", "Part-time", "Freelance")


def populate_table(apps: Any, schema_editor: Any) -> None:
    """Populates table with default values."""
    for value in DEFAULT_VALUES:
        WorkFormat.objects.create(name=value)


def reverse_table_population(apps: Any, schema_editor: Any) -> None:
    """Reverse table population."""
    for value in DEFAULT_VALUES:
        WorkFormat.objects.get(name=value).delete()


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ("core", "0004_populate_employment_format_table"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_table,
            reverse_code=reverse_table_population,
        )
    ]
