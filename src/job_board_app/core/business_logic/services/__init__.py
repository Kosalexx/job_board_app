"""All methods and functions of services package."""

from .common import change_file_size, replace_file_name_to_uuid
from .company import (
    create_company,
    get_companies,
    get_company_by_id,
    get_company_profile_by_id,
    get_vacancies_by_company_id,
)
from .country import get_countries
from .employment_formats import get_employment_formats
from .groups import get_groups
from .levels import get_levels
from .login import authenticate_user
from .registration import confirm_user_registration, create_user
from .response import get_response_status_by_name
from .vacancy import apply_to_vacancy, create_vacancy, get_vacancy_by_id, search_vacancies
from .work_formats import get_work_formats

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
    "confirm_user_registration",
    "authenticate_user",
    "get_countries",
    "get_groups",
    "get_levels",
    "get_employment_formats",
    "get_work_formats",
    "apply_to_vacancy",
    "get_response_status_by_name",
]
