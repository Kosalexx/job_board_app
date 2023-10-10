"""
DTO package attributes, classes, and functions.
"""

from .company import AddAddressDTO, AddCompanyDTO, AddCompanyProfileDTO
from .login import LoginDTO
from .registration import RegistrationDTO
from .vacancy import AddVacancyDTO, ApplyVacancyDTO, SearchVacancyDTO, VacancyDataDTO

__all__ = [
    "SearchVacancyDTO",
    "AddVacancyDTO",
    "AddCompanyDTO",
    "AddCompanyProfileDTO",
    "AddAddressDTO",
    "RegistrationDTO",
    "LoginDTO",
    "ApplyVacancyDTO",
    "VacancyDataDTO",
]
