"""
Forms package attributes, classes, and functions.
"""

from .company import AddAddressFrom, AddCompanyForm, CompanyProfileForm
from .login import LoginForm
from .registration import RegistrationForm
from .vacancy import AddVacancyForm, ApplyVacancyForm, SearchVacancyForm

__all__ = [
    "AddVacancyForm",
    "AddCompanyForm",
    "SearchVacancyForm",
    "CompanyProfileForm",
    "AddAddressFrom",
    "RegistrationForm",
    "LoginForm",
    "ApplyVacancyForm",
]
