"""
Functions and methods for converting data from form to the DTO.
"""

from typing import TypeVar

from core.business_logic.dto import (
    AddAddressDTO,
    AddCompanyDTO,
    AddCompanyProfileDTO,
    AddVacancyDTO,
    SearchVacancyDTO,
)
from dacite import from_dict

T = TypeVar('T', AddAddressDTO, AddCompanyDTO, AddCompanyProfileDTO, AddVacancyDTO, SearchVacancyDTO)


def convert_data_from_form_to_dto(dto: type[T], data_from_form: dict) -> T:
    """Converts data form form to the DTO."""

    result: T = from_dict(dto, data_from_form)
    return result
