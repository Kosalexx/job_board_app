"""
"Core" app Company models of job_board_app project.
"""
from __future__ import annotations

from django.db import models

from .base import BaseModel


def company_directory_path(instance: "CompanyProfile", filename: str) -> str:
    """Provides a path to directory with files of specific company."""

    return f'companies_media/company_{instance.company.id,}/{filename}'


class CompanyProfile(BaseModel):
    """Describes the fields and attributes of the Company_Profile model in the database."""

    logo = models.ImageField(upload_to=company_directory_path, null=True)
    email = models.EmailField(null=False)
    founding_year = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=800)
    phone = models.CharField(max_length=30)
    website_link = models.CharField(max_length=100, null=False)
    linkedin_link = models.CharField(max_length=100, null=True)
    github_link = models.CharField(max_length=100, null=True)
    twitter_link = models.CharField(max_length=100, null=True)
    address = models.ForeignKey(
        to='Address',
        on_delete=models.CASCADE,
        related_name='company_profiles',
        related_query_name='company_profile',
        default=None,
    )
    company = models.OneToOneField(
        to='Company',
        on_delete=models.CASCADE,
        related_name='company_profiles',
        related_query_name='company_profile',
        primary_key=True,
    )

    class Meta:
        """Describes class metadata."""

        db_table = "company_profiles"


# Create your models here.
class Company(BaseModel):
    """Describes the fields and attributes of the Company model in the database."""

    name = models.CharField(unique=True, max_length=100)
    staff = models.PositiveIntegerField(default=0)

    business_area = models.ManyToManyField(
        to="BusinessArea", related_name='companies', related_query_name='company', db_table='company_business_areas'
    )

    class Meta:
        """Describes class metadata."""

        db_table = "companies"
