from typing import Any

from core.models import LanguageLevel
from django.db import migrations

DEFAULT_VALUES = ("Beginner", "Elementary", "Intermediate", "Upper-Intermediate", "Advanced", "Proficiency", "Native")


def populate_table(apps: Any, schema_editor: Any) -> None:
    for value in DEFAULT_VALUES:
        LanguageLevel.objects.create(name=value)


def reverse_table_population(apps: Any, schema_editor: Any) -> None:
    for value in DEFAULT_VALUES:
        LanguageLevel.objects.get(name=value).delete()


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ("core", "0004_alter_company_profile_staff_delete_staff"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_table,
            reverse_code=reverse_table_population,
        )
    ]
