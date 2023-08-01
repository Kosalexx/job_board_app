"""
DTO package attributes, classes, and functions.
"""

from .company import AddAddressDTO, AddCompanyDTO, AddCompanyProfileDTO
from .registration import RegistrationDTO
from .vacancy import AddVacancyDTO, SearchVacancyDTO

__all__ = [
    "SearchVacancyDTO",
    "AddVacancyDTO",
    "AddCompanyDTO",
    "AddCompanyProfileDTO",
    "AddAddressDTO",
    "RegistrationDTO",
]
