"""
Data transfer objects related to the AddVacancyFrom, SearchVacancyFrom forms.

DTOs are designed to move data between processes to reduce the number of method calls.
AddVacancyForm, SearchVacancyFrom forms are described in the core.presentation.web.forms.vacancy module.
"""

from dataclasses import dataclass

from core.models import City, EmploymentFormat, Tag, Vacancy, WorkFormat
from django.contrib.auth.models import AbstractBaseUser
from django.core.files.uploadedfile import InMemoryUploadedFile


@dataclass
class SearchVacancyDTO:
    """DTO for storing and transferring data from SearchVacancyForm."""

    name: str
    company_name: str
    level: str
    experience: str
    description: str | None
    min_salary: int | None
    max_salary: int | None
    employment_format: list
    work_format: list
    country: str
    city: str
    tag: str


@dataclass
class AddVacancyDTO:
    """DTO for storing and transferring data from AddVacancyForm."""

    name: str
    company_name: str
    level: str
    experience: str
    description: str | None
    min_salary: int | None
    max_salary: int | None
    employment_format: list
    work_format: list
    country: str
    city: str
    tags: str
    attachment: InMemoryUploadedFile | None


@dataclass
class VacancyDataDTO:
    """DTO for storing and transferring data about vacancy info from DB."""

    vacancy: Vacancy
    tags: list[Tag]
    employment_format: list[EmploymentFormat]
    work_format: list[WorkFormat]
    city: list[City]


@dataclass
class ApplyVacancyDTO:
    """DTO for storing and transferring data from ApplyVacancyForm."""

    user: AbstractBaseUser | None
    vacancy: Vacancy | None
    cover_note: str
    cv: InMemoryUploadedFile | None
