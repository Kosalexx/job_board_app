"""
API Views (controllers) for job_board_app that related with company logic.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.exceptions import CompanyNotExistsError
from core.business_logic.services import get_companies, get_company_by_id
from core.presentation.api_v1.serializers import CompaniesListSerializer, CompanyExtendedInfoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

if TYPE_CHECKING:
    from rest_framework.request import Request


@api_view(http_method_names=['GET'])
def get_companies_api_controller(request: Request) -> Response:
    """API controller that returns list of all vacancies."""
    companies = get_companies()
    companies_serializer = CompaniesListSerializer(companies, many=True)
    return Response(data=companies_serializer.data)


@api_view(http_method_names=['GET'])
def get_company_api_controller(request: Request, company_id: int) -> Response:
    """API controller that returns specific company with entered id."""

    try:
        company = get_company_by_id(company_id=company_id)
    except CompanyNotExistsError:
        data = {"message": "Company with provided id doesn't exist."}
        return Response(data=data, status=HTTP_404_NOT_FOUND)
    company_serializer = CompanyExtendedInfoSerializer(company)
    return Response(data=company_serializer.data)
