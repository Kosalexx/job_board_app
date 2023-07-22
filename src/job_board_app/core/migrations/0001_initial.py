""" Initial migrations.
Generated by Django 4.2.2 on 2023-07-13 14:16 """

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    initial = True

    dependencies: list = []

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
                ('home_number', models.PositiveSmallIntegerField()),
                ('office_number', models.PositiveSmallIntegerField()),
            ],
            options={
                'db_table': 'addresses',
            },
        ),
        migrations.CreateModel(
            name='Business_area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'business_areas',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'db_table': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('logo_link', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=254)),
                (
                    'address',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='companies',
                        related_query_name='company',
                        to='core.address',
                    ),
                ),
                (
                    'business_area',
                    models.ManyToManyField(
                        db_table='company_business_areas',
                        related_name='companies',
                        related_query_name='company',
                        to='core.business_area',
                    ),
                ),
            ],
            options={
                'db_table': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'db_table': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Employment_format',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'db_table': 'employment_formats',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'db_table': 'languages',
            },
        ),
        migrations.CreateModel(
            name='Language_level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'db_table': 'language_levels',
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'levels',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'positions',
            },
        ),
        migrations.CreateModel(
            name='Response_status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'db_table': 'response_statuses',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('range_start', models.PositiveIntegerField()),
                ('range_end', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'staff',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('photo_link', models.CharField(blank=True, max_length=100, unique=True)),
                ('summary_link', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=254)),
                (
                    'employment_format',
                    models.ManyToManyField(
                        db_table='users_employment_formats',
                        related_name='users',
                        related_query_name='user',
                        to='core.employment_format',
                    ),
                ),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Work_format',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'db_table': 'work_formats',
            },
        ),
        migrations.CreateModel(
            name='Work_status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'db_table': 'work_statuses',
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('experience', models.CharField(max_length=30)),
                ('min_salary', models.PositiveIntegerField(null=True)),
                ('max_salary', models.PositiveIntegerField(null=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField()),
                ('city', models.ManyToManyField(db_table='vacancy_cities', related_name='vacancies', to='core.city')),
                (
                    'company',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='vacancies',
                        related_query_name='vacancy',
                        to='core.company',
                    ),
                ),
                (
                    'employment_format',
                    models.ManyToManyField(
                        db_table='vacancy_employment_formats', related_name='vacancies', to='core.employment_format'
                    ),
                ),
                (
                    'level',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='vacancies',
                        related_query_name='vacancy',
                        to='core.level',
                    ),
                ),
                ('tags', models.ManyToManyField(db_table='vacancies_tags', related_name='vacancies', to='core.tag')),
                (
                    'work_format',
                    models.ManyToManyField(
                        db_table='vacancy_work_formats', related_name='vacancies', to='core.work_format'
                    ),
                ),
            ],
            options={
                'db_table': 'vacancies',
            },
        ),
        migrations.CreateModel(
            name='Users_profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('login', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=30)),
                ('age', models.PositiveSmallIntegerField()),
                ('experience_description', models.CharField(max_length=800)),
                ('linkedin_link', models.CharField(blank=True, max_length=100)),
                ('github_link', models.CharField(blank=True, max_length=100)),
                ('work_experience', models.IntegerField(blank=True)),
                ('min_salary', models.PositiveIntegerField(null=True)),
                ('max_salary', models.PositiveIntegerField(null=True)),
                (
                    'city',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='users_profiles',
                        related_query_name='users_profile',
                        to='core.city',
                    ),
                ),
                (
                    'level',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='users_profiles',
                        related_query_name='users_profile',
                        to='core.level',
                    ),
                ),
            ],
            options={
                'db_table': 'users_profiles',
            },
        ),
        migrations.CreateModel(
            name='Users_languages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                (
                    'language',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='users_languages',
                        related_query_name='users_language',
                        to='core.language',
                    ),
                ),
                (
                    'language_level',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='users_languages',
                        related_query_name='users_language',
                        to='core.language_level',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='users_languages',
                        related_query_name='users_language',
                        to='core.user',
                    ),
                ),
            ],
            options={
                'db_table': 'users_languages',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='profile',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='users',
                related_query_name='user',
                to='core.users_profile',
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='tags',
            field=models.ManyToManyField(
                db_table='users_tags', related_name='users', related_query_name='user', to='core.tag'
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='user_language',
            field=models.ManyToManyField(through='core.Users_languages', to='core.language'),
        ),
        migrations.AddField(
            model_name='user',
            name='work_format',
            field=models.ManyToManyField(
                db_table='users_work_formats', related_name='users', related_query_name='user', to='core.work_format'
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='work_status',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='users',
                related_query_name='user',
                to='core.work_status',
            ),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(max_length=800)),
                ('likes_counter', models.PositiveIntegerField(default=0)),
                ('dislike_counter', models.PositiveIntegerField(default=0)),
                (
                    'company',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='reviews',
                        related_query_name='review',
                        to='core.company',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='reviews',
                        related_query_name='review',
                        to='core.user',
                    ),
                ),
            ],
            options={
                'db_table': 'reviews',
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cover_note', models.CharField(max_length=500)),
                ('summary_link', models.CharField()),
                ('user_phone', models.CharField(max_length=30)),
                (
                    'response_status',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='responses',
                        related_query_name='response',
                        to='core.response_status',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='responses',
                        related_query_name='response',
                        to='core.user',
                    ),
                ),
                (
                    'vacancy',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='responses',
                        related_query_name='response',
                        to='core.vacancy',
                    ),
                ),
            ],
            options={
                'db_table': 'responses',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=50)),
                ('photo_link', models.CharField(blank=True)),
                (
                    'city',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='employees',
                        related_query_name='employee',
                        to='core.city',
                    ),
                ),
                (
                    'company',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='employees',
                        related_query_name='employee',
                        to='core.company',
                    ),
                ),
                (
                    'position',
                    models.ManyToManyField(db_table='employee_positions', related_name='employees', to='core.position'),
                ),
            ],
            options={
                'db_table': 'employees',
            },
        ),
        migrations.CreateModel(
            name='Company_Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('founding_year', models.PositiveSmallIntegerField()),
                ('description', models.CharField(max_length=800)),
                ('phone', models.CharField(max_length=30)),
                ('website_link', models.CharField(max_length=100)),
                ('linkedin_link', models.CharField(blank=True, max_length=100)),
                ('github_link', models.CharField(blank=True, max_length=100)),
                ('twitter_link', models.CharField(blank=True, max_length=100)),
                (
                    'staff',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='company_profiles',
                        related_query_name='company_profile',
                        to='core.staff',
                    ),
                ),
            ],
            options={
                'db_table': 'company_profiles',
            },
        ),
        migrations.AddField(
            model_name='company',
            name='company_profile',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='companies',
                related_query_name='company',
                to='core.company_profile',
            ),
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='cities',
                related_query_name='city',
                to='core.country',
            ),
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='addresses',
                related_query_name='address',
                to='core.city',
            ),
        ),
    ]
