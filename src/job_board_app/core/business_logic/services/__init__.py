"""All methods and functions of services package."""

from .common import change_file_size, replace_file_name_to_uuid
from .company import (
    create_company,
    get_companies,
    get_company_by_id,
    get_company_profile_by_id,
    get_vacancies_by_company_id,
)
from .registration import create_user
from .vacancy import create_vacancy, get_vacancy_by_id, search_vacancies

__all__ = [
    "create_company",
    "get_companies",
    "get_company_by_id",
    "get_company_profile_by_id",
    "change_file_size",
    "search_vacancies",
    "get_vacancy_by_id",
    "create_vacancy",
    "replace_file_name_to_uuid",
    "get_vacancies_by_company_id",
    "create_user",
]
