"""
Alter staff range end migration.
Generated by Django 4.2.3 on 2023-07-17 21:06
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ('core', '0002_populate_level_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='range_end',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
