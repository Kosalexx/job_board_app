"""
Custom migration that populate Levels table with default values.
"""

from typing import Any

from core.models import Level
from django.db import migrations

DEFAULT_LEVELS = ("Intern", "Junior", "Middle", "Senior")


def populate_levels_table(apps: Any, schema_editor: Any) -> None:
    """Populates table with default values."""
    for level in DEFAULT_LEVELS:
        Level.objects.create(name=level)


def reverse_table_population(apps: Any, schema_editor: Any) -> None:
    """Reverse table population."""
    for level in DEFAULT_LEVELS:
        Level.objects.get(name=level).delete()


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_levels_table,
            reverse_code=reverse_table_population,
        )
    ]
