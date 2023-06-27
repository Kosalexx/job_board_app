"""
Services and business logic for "core" app job_board_app project.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional


@dataclass
class Vacancy:
    """A dataclass for storing and transmitting data about a vacancy."""

    name: str
    company: str
    level: str
    experience: str
    min_salary: int | None
    max_salary: int | None
    id: int | None = None  # noqa: A003 pylint: disable=C0103


@dataclass
class Company:
    """A dataclass for storing and transmitting data about a company."""

    name: str
    employees_number: int
    vacancies_counter: int = 0
    id: int | None = None  # noqa: A003 pylint: disable=C0103


class CompanyDuplicateNameError(Exception):
    """Exception that is caused if a company with entered name already exist."""


class CompanyNotExistError(Exception):
    """Exception that is caused if a company with entered name doesn't exist in database."""


class BaseStorage:  # pylint: disable=too-few-public-methods
    """Base storage class for storing and work with Vacancies or Companies data."""

    ID_COUNT = 0

    def update_counter(self) -> int:
        """Updates ID counter by 1."""
        self.ID_COUNT += 1  # pylint: disable=C0103
        return self.ID_COUNT  # pylint: disable=C0103


class CompanyStorage(BaseStorage):
    """Company storage class for storing and work with Companies data."""

    def __init__(self) -> None:
        self._companies: list[Company] = []

    def _validate_company(self, company_to_add: Company) -> None:
        """Validates company data based on company.name.

        :param company_to_add: Company DTO
        :type company_to_add: class Company

        :raises CompanyDuplicateNameError: if company.name.lower() already exist in database

        :return type: None
        """
        for company in self._companies:
            if company.name.lower() == company_to_add.name.lower():
                raise CompanyDuplicateNameError

    def add_company(self, company_to_add: Company) -> None:
        """Add company data to the database.

        :param company_to_add: Company DTO
        :type company_to_add: class Company

        :return type: None
        """
        self._validate_company(company_to_add=company_to_add)
        primary_key = self.update_counter()
        company_to_add.id = primary_key
        self._companies.append(company_to_add)

    def get_all_companies(self) -> list[Company]:
        """Returns list of all companies in the database.

        :return type: list[Company]
        :return: list of Company DTO with data about all companies in database
        """
        return self._companies

    def get_company_by_name(self, company_name: str) -> Optional[Company]:
        """Returns company DTO based on entered company name.

        :param company_name: name of searched company
        :type company_name: str

        :return type: Optional[Company]
        :return: Company DTO with data about searched company
        """
        for company in self._companies:
            if company.name.lower() == company_name.lower():
                return company
        return None


class VacancyStorage(BaseStorage):
    """Vacancy storage class for storing and work with vacancies data."""

    def __init__(self, company_storage: CompanyStorage) -> None:
        self._vacancies: list[Vacancy] = []
        self._company_storage = company_storage

    def add_vacancy(self, vacancy_to_add: Vacancy) -> None:
        """Add vacancy data to the database.

        :param vacancy_to_add: Vacancy DTO
        :type vacancy_to_add: class Vacancy

        :return type: None
        """
        company = self._company_storage.get_company_by_name(company_name=vacancy_to_add.company)
        if not company:
            raise CompanyNotExistError
        primary_key = self.update_counter()
        vacancy_to_add.id = primary_key
        self._vacancies.append(vacancy_to_add)
        company.vacancies_counter += 1

    def get_all_vacancies(self) -> list[Vacancy]:
        """Returns list of all vacancies in the database.

        :return type: list[Vacancy]
        :return: list of Vacancy DTO with data about all vacancies in database
        """
        return self._vacancies
