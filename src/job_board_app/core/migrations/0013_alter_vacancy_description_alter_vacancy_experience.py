# Generated by Django 4.2.3 on 2023-10-24 20:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0012_alter_address_office_number_alter_city_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='description',
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='experience',
            field=models.CharField(max_length=30, null=True),
        ),
    ]