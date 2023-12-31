"""
Functions and methods for converting data from form to the DTO.
"""

from typing import TypeVar

from core.business_logic.dto import (
    AddAddressDTO,
    AddCompanyDTO,
    AddCompanyProfileDTO,
    AddVacancyDTO,
    ApplyVacancyDTO,
    LoginDTO,
    RegistrationDTO,
    SearchVacancyDTO,
)
from dacite import from_dict

T = TypeVar(
    'T',
    AddAddressDTO,
    AddCompanyDTO,
    AddCompanyProfileDTO,
    AddVacancyDTO,
    SearchVacancyDTO,
    RegistrationDTO,
    LoginDTO,
    ApplyVacancyDTO,
)


def convert_data_from_request_to_dto(dto: type[T], data_from_request: dict) -> T:
    """Converts data form form to the DTO."""

    result: T = from_dict(dto, data_from_request)
    return result
