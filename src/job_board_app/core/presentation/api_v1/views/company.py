"""
API Views (controllers) for job_board_app that related with company logic.
"""
from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from core.business_logic.dto import AddAddressDTO, AddCompanyDTO, AddCompanyProfileDTO
from core.business_logic.exceptions import CompanyNotExistsError
from core.business_logic.services import create_company, get_companies, get_company_by_id
from core.presentation.api_v1.serializers import (
    AddCompanySerializer,
    CompaniesListSerializer,
    CompanyExtendedInfoSerializer,
)
from core.presentation.common.converters import convert_data_from_request_to_dto
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

if TYPE_CHECKING:
    from rest_framework.request import Request


logger = getLogger(__name__)


@api_view(http_method_names=['GET', 'POST'])
def companies_api_controller(request: Request) -> Response:
    """API controller that returns list of all vacancies."""
    if request.method == 'GET':
        companies = get_companies()
        companies_serializer = CompaniesListSerializer(companies, many=True)
        return Response(data=companies_serializer.data)
    else:
        add_company_serializer = AddCompanySerializer(data=request.data)
        if add_company_serializer.is_valid():
            company_dto = convert_data_from_request_to_dto(AddCompanyDTO, add_company_serializer.validated_data)
            company_profile_dto = convert_data_from_request_to_dto(
                AddCompanyProfileDTO, add_company_serializer.validated_data
            )
            address_dto = convert_data_from_request_to_dto(AddAddressDTO, add_company_serializer.validated_data)
            company_id = create_company(
                company_data=company_dto, profile_data=company_profile_dto, address_data=address_dto
            )
        else:
            logger.warning(f'The forms have not been validated. Errors: {add_company_serializer.errors}')
            return Response(data=add_company_serializer.errors, status=HTTP_400_BAD_REQUEST)
        data = {"message": "Company created successfully", "company_id": company_id}
        return Response(data=data)


@api_view(http_method_names=['GET'])
def company_api_controller(request: Request, company_id: int) -> Response:
    """API controller that returns specific company with entered id."""

    try:
        company = get_company_by_id(company_id=company_id)
    except CompanyNotExistsError:
        data = {"message": "Company with provided id doesn't exist."}
        return Response(data=data, status=HTTP_404_NOT_FOUND)
    company_serializer = CompanyExtendedInfoSerializer(company)
    return Response(data=company_serializer.data)
