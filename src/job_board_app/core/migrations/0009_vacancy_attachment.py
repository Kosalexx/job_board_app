"""
Added attachment field into the vacancy table.
Generated by Django 4.2.3 on 2023-07-19 17:26
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ('core', '0008_populate_work_formats_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='attachment',
            field=models.FileField(null=True, upload_to='vacancy_attachments/'),
        ),
    ]