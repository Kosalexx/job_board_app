"""
Removed fields form Company table to the CompanyProfile table.
Generated by Django 4.2.3 on 2023-07-20 15:22
"""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ('core', '0012_populate_country_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='company_profile',
        ),
        migrations.RemoveField(
            model_name='company_profile',
            name='id',
        ),
        migrations.AddField(
            model_name='company_profile',
            name='company',
            field=models.OneToOneField(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                related_name='company_profiles',
                related_query_name='company_profile',
                serialize=False,
                to='core.company',
            ),
            preserve_default=False,
        ),
    ]
