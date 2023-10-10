"""
Custom migration that adds apply vacancy permission to candidate.
"""

from typing import Any

from django.contrib.auth.models import Group, Permission
from django.db import migrations

DEFAULT_VALUES = {"candidate": [], "recruiter": ['add_vacancy', 'add_company']}


def add_permission_to_candidate(apps: Any, schema_editor: Any) -> None:
    """Adds apply vacancy permission to candidate."""
    group = Group.objects.get(name='candidate')
    permission = Permission.objects.filter(codename='apply_to_vacancy')
    group.permissions.set(permission)


def drop_permission(apps: Any, schema_editor: Any) -> None:
    """Reverse migration."""
    group = Group.objects.get(name='candidate')
    permission = Permission.objects.filter(codename='apply_to_vacancy')
    group.permissions.remove(permission)


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ("core", "0008_alter_vacancy_options"),
    ]

    operations = [
        migrations.RunPython(
            code=add_permission_to_candidate,
            reverse_code=drop_permission,
        )
    ]
