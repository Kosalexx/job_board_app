"""
Custom migration that populate LanguageLevels table with default values.
"""

from typing import Any

from core.models import EmploymentFormat
from django.db import migrations

DEFAULT_VALUES = ("Employment contract", "B2B", "Mandate contract")


def populate_table(apps: Any, schema_editor: Any) -> None:
    """Populates table with default values."""
    for value in DEFAULT_VALUES:
        EmploymentFormat.objects.create(name=value)


def reverse_table_population(apps: Any, schema_editor: Any) -> None:
    """Reverse table population."""
    for value in DEFAULT_VALUES:
        EmploymentFormat.objects.get(name=value).delete()


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ("core", "0003_populate_language_levels_table"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_table,
            reverse_code=reverse_table_population,
        )
    ]
