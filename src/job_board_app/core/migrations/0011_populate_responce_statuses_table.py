"""
Custom migration that populate ResponseStatuses table with default values.
"""

from typing import Any

from core.models import ResponseStatus
from django.db import migrations

DEFAULT_VALUES = ("New", "Viewed", "Denied", "Accepted to work")


def populate_table(apps: Any, schema_editor: Any) -> None:
    """Populates table with default values."""
    for value in DEFAULT_VALUES:
        ResponseStatus.objects.create(name=value)


def reverse_table_population(apps: Any, schema_editor: Any) -> None:
    """Reverse table population."""
    for value in DEFAULT_VALUES:
        ResponseStatus.objects.get(name=value).delete()


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ("core", "0010_remove_response_summary_link_and_more"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_table,
            reverse_code=reverse_table_population,
        )
    ]
