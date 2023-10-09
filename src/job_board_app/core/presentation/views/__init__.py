"""Views package initial attributes, classes, and functions."""

from .company import add_company_controller, companies_list_controller, get_company_controller
from .login import login_controller
from .logout import logout_controller
from .registration import registration_confirmation, registration_controller
from .vacancy import add_vacancy_controller, get_vacancy_controller, index_controller

__all__ = [
    "add_company_controller",
    "get_company_controller",
    "companies_list_controller",
    "index_controller",
    "add_vacancy_controller",
    "get_vacancy_controller",
    "registration_controller",
    "registration_confirmation",
    "login_controller",
    "logout_controller",
]
