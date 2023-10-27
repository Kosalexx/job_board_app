"""
"Core" app Vacancy model of job_board_app project.
"""

from django.db import models

from .base import BaseModel


def vacancy_attachments_directory_path(instance: "Vacancy", filename: str) -> str:
    """Provides a path to directory with attachments of specific vacancy."""

    return f'vacancy_attachments/company_{instance.company.id}/({instance.name})_{instance.level.name}/{filename}'


def vacancy_qr_codes_directory_path(instance: "Vacancy", filename: str) -> str:
    """Provides a path to directory with qr codes of specific vacancy."""

    return f'vacancy_qr/company_{instance.company.id}/({instance.name})_{instance.level.name}/{filename}'


class Vacancy(BaseModel):
    """Describes the fields and attributes of the Vacancy model in the database."""

    level = models.ForeignKey(
        to='Level', on_delete=models.CASCADE, related_name='vacancies', related_query_name='vacancy'
    )
    experience = models.CharField(max_length=30, null=True)
    min_salary = models.PositiveIntegerField(null=True)
    max_salary = models.PositiveIntegerField(null=True)
    company = models.ForeignKey(
        to='Company', on_delete=models.CASCADE, related_name='vacancies', related_query_name='vacancy'
    )
    tags = models.ManyToManyField(to="Tag", related_name='vacancies', db_table='vacancies_tags')
    name = models.CharField(max_length=100)
    description = models.CharField(null=True)
    employment_format = models.ManyToManyField(
        to="EmploymentFormat", related_name='vacancies', db_table='vacancy_employment_formats'
    )
    work_format = models.ManyToManyField(to="WorkFormat", related_name='vacancies', db_table='vacancy_work_formats')
    city = models.ManyToManyField(to='City', related_name='vacancies', db_table='vacancy_cities')
    attachment = models.FileField(upload_to=vacancy_attachments_directory_path, null=True)
    qr_code = models.ImageField(upload_to=vacancy_qr_codes_directory_path, null=True)

    class Meta:
        """Describes class metadata."""

        db_table = "vacancies"
        permissions = [
            ('apply_to_vacancy', 'Allows apply to any vacancy'),
        ]
