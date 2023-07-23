"""
Data transfer objects related to the AddVacancyFrom, SearchVacancyFrom forms.

DTOs are designed to move data between processes to reduce the number of method calls.
AddVacancyForm, SearchVacancyFrom forms are described in the core.presentation.forms.vacancy module.
"""

from dataclasses import dataclass

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
