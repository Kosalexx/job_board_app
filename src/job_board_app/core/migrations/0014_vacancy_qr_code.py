# Generated by Django 4.2.3 on 2023-10-27 12:02

import core.models.vacancy
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0013_alter_vacancy_description_alter_vacancy_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='qr_code',
            field=models.ImageField(null=True, upload_to=core.models.vacancy.vacancy_qr_codes_directory_path),
        ),
    ]
