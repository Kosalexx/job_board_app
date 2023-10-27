"""
API Views (controllers) for job_board_app that related with company logic.
"""
from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from core.business_logic.dto import AddAddressDTO, AddCompanyDTO, AddCompanyProfileDTO
from core.business_logic.exceptions import CompanyAlreadyExistsError, CompanyNotExistsError, CountryNotExistError
from core.business_logic.services import create_company, get_companies, get_company_by_id
from core.presentation.api_v1.serializers import (
    AddCompanyResponseSerializer,
    AddCompanySerializer,
    CompanyExtendedInfoSerializer,
    CompanyInfoSerializer,
    ErrorSerializer,
)
from core.presentation.common.converters import convert_data_from_request_to_dto
from django.contrib.auth.decorators import permission_required
from django.views.decorators.cache import cache_page
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers
from rest_framework.decorators import api_view, parser_classes, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.throttling import UserRateThrottle

if TYPE_CHECKING:
    from rest_framework.request import Request


logger = getLogger(__name__)


@swagger_auto_schema(
    method="POST",
    manual_parameters=[
        openapi.Parameter(
            name="name", description="Copmany name", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True
        ),
        openapi.Parameter(name="staff", in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER, required=True),
        openapi.Parameter(name="business_area", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
        openapi.Parameter(name="logo", in_=openapi.IN_FORM, type=openapi.TYPE_FILE),
        openapi.Parameter(name="email", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
        openapi.Parameter(name="founding_year", in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER, required=True),
        openapi.Parameter(name="description", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
        openapi.Parameter(name="phone", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
        openapi.Parameter(name="website_link", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
        openapi.Parameter(name="linkedin_link", in_=openapi.IN_FORM, type=openapi.TYPE_STRING),
        openapi.Parameter(name="github_link", in_=openapi.IN_FORM, type=openapi.TYPE_STRING),
        openapi.Parameter(name="twitter_link", in_=openapi.IN_FORM, type=openapi.TYPE_STRING),
        openapi.Parameter(name="country", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
        openapi.Parameter(name="city", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
        openapi.Parameter(name="street_name", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
        openapi.Parameter(name="home_number", in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER, required=True),
        openapi.Parameter(name="office_number", in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER),
    ],
    responses={
        200: openapi.Response(description="Successfully response", schema=AddCompanyResponseSerializer),
        400: openapi.Response(description="Provided invalid data"),
        500: openapi.Response(description="Unhandled server error"),
    },
)
@swagger_auto_schema(
    method="GET",
    responses={
        200: openapi.Response(description="Successfully response", schema=CompanyInfoSerializer(many=True)),
        500: openapi.Response(description="Unhandled server error"),
    },
)
@api_view(http_method_names=['GET', 'POST'])
@cache_page(10)
@permission_required(["core.add_company"])
@permission_classes([IsAuthenticated])
@parser_classes([parsers.MultiPartParser])
def companies_api_controller(request: Request) -> Response:
    """API controller that returns list of all vacancies."""
    if request.method == 'GET':
        companies = get_companies()
        companies_serializer = CompanyInfoSerializer(companies, many=True)
        return Response(data=companies_serializer.data)
    else:
        add_company_serializer = AddCompanySerializer(data=request.data)
        if add_company_serializer.is_valid():
            company_dto = convert_data_from_request_to_dto(AddCompanyDTO, add_company_serializer.validated_data)
            company_profile_dto = convert_data_from_request_to_dto(
                AddCompanyProfileDTO, add_company_serializer.validated_data
            )
            address_dto = convert_data_from_request_to_dto(AddAddressDTO, add_company_serializer.validated_data)
            try:
                company_id = create_company(
                    company_data=company_dto, profile_data=company_profile_dto, address_data=address_dto
                )
            except CompanyAlreadyExistsError:
                error_data = {"message": "Company with provided name already exist in the database."}
                return Response(data=error_data, status=HTTP_400_BAD_REQUEST)
            except CountryNotExistError:
                error_data = {"message": "Country with provided name does not exist in the database."}
                return Response(data=error_data, status=HTTP_400_BAD_REQUEST)
        else:
            logger.warning(f'The forms have not been validated. Errors: {add_company_serializer.errors}')
            return Response(data=add_company_serializer.errors, status=HTTP_400_BAD_REQUEST)

        data = {"message": "Company created successfully", "company_id": company_id}
        result = AddCompanyResponseSerializer(data)
        return Response(data=result.data)


@swagger_auto_schema(
    method="GET",
    manual_parameters=[openapi.Parameter(name="company_id", in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER)],
    responses={
        200: openapi.Response(description="Successfully response", schema=CompanyExtendedInfoSerializer(many=True)),
        500: openapi.Response(description="Unhandled server error"),
        404: openapi.Response(description="Resource not found", schema=ErrorSerializer),
    },
)
@api_view(http_method_names=['GET'])
@throttle_classes([UserRateThrottle])
@permission_classes([IsAuthenticated])
def company_api_controller(request: Request, company_id: int) -> Response:
    """API controller that returns specific company with entered id."""

    try:
        company = get_company_by_id(company_id=company_id)
    except CompanyNotExistsError:
        data = {"message": "Company with provided id doesn't exist."}
        return Response(data=data, status=HTTP_404_NOT_FOUND)
    company_serializer = CompanyExtendedInfoSerializer(company)
    return Response(data=company_serializer.data)
