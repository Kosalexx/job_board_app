"""
Custom migration that populate WorkStatuses table with default values.
"""

from typing import Any

from core.models import WorkStatus
from django.db import migrations

DEFAULT_VALUES = ("Open to work", "Open for proposals", "Not open for proposals")


def populate_table(apps: Any, schema_editor: Any) -> None:
    """Populates table with default values."""
    for value in DEFAULT_VALUES:
        WorkStatus.objects.create(name=value)


def reverse_table_population(apps: Any, schema_editor: Any) -> None:
    """Reverse table population."""
    for value in DEFAULT_VALUES:
        WorkStatus.objects.get(name=value).delete()


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ("core", "0006_populate_employment_format_table"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_table,
            reverse_code=reverse_table_population,
        )
    ]
