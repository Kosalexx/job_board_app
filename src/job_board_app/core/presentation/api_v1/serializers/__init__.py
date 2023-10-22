"""
API serializers package attributes, classes, and functions.
"""
from .common import ErrorSerializer
from .company import (
    AddCompanyResponseSerializer,
    AddCompanySerializer,
    CompanyExtendedInfoSerializer,
    CompanyInfoSerializer,
)
from .vacancy import (
    AddVacancyResponseSerializer,
    AddVacancySerializer,
    SearchVacancySerializer,
    VacancyExtendedInfoSerializer,
    VacancyInfoPaginatedResponseSerializer,
    VacancyInfoSerializer,
)

__all__ = [
    "SearchVacancySerializer",
    "VacancyInfoSerializer",
    "CompanyInfoSerializer",
    "VacancyExtendedInfoSerializer",
    "CompanyExtendedInfoSerializer",
    "AddCompanySerializer",
    "AddVacancySerializer",
    "AddCompanyResponseSerializer",
    "ErrorSerializer",
    "AddVacancyResponseSerializer",
    "VacancyInfoPaginatedResponseSerializer",
]
