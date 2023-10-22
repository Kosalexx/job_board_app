"""
API Views (controllers) for job_board_app that related with vacancy logic.
"""
from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from core.business_logic.dto import AddVacancyDTO, SearchVacancyDTO
from core.business_logic.exceptions import VacancyNotExistsError
from core.business_logic.services import create_vacancy, get_vacancy_by_id, search_vacancies
from core.presentation.api_v1.pagination import APIPaginator
from core.presentation.api_v1.serializers import (
    AddVacancyResponseSerializer,
    AddVacancySerializer,
    ErrorSerializer,
    SearchVacancySerializer,
    VacancyExtendedInfoSerializer,
    VacancyInfoPaginatedResponseSerializer,
    VacancyInfoSerializer,
)
from core.presentation.common.converters import convert_data_from_request_to_dto
from django.contrib.auth.decorators import permission_required
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

if TYPE_CHECKING:
    from rest_framework.request import Request


logger = getLogger(__name__)


@swagger_auto_schema(
    method="POST",
    manual_parameters=[
        openapi.Parameter(
            name="name", description="Vacancy name", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True
        ),
        openapi.Parameter(name="company_name", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
        openapi.Parameter(name="level", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
        openapi.Parameter(name="experience", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
        openapi.Parameter(name="min_salary", in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER, required=False),
        openapi.Parameter(name="max_salary", in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER, required=False),
        openapi.Parameter(name="description", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
        openapi.Parameter(
            name="employment_format",
            in_=openapi.IN_FORM,
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING),
            required=True,
        ),
        openapi.Parameter(
            name="work_format",
            in_=openapi.IN_FORM,
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING),
            required=True,
        ),
        openapi.Parameter(name="country", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
        openapi.Parameter(name="city", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
        openapi.Parameter(name="tags", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
        openapi.Parameter(name="attachment", in_=openapi.IN_FORM, type=openapi.TYPE_FILE, required=False),
    ],
    responses={
        200: openapi.Response(description="Successfully response", schema=AddVacancyResponseSerializer),
        400: openapi.Response(description="Provided invalid data"),
        500: openapi.Response(description="Unhandled server error"),
    },
)
@swagger_auto_schema(
    method="GET",
    manual_parameters=[
        openapi.Parameter(name="page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter(name="name", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter(name="company_name", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter(name="level", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter(name="experience", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter(name="min_salary", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter(name="max_salary", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter(name="tag", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter(
            name="employment_format",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING),
        ),
        openapi.Parameter(
            name="work_format",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING),
        ),
        openapi.Parameter(name="country", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter(name="city", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ],
    responses={
        200: openapi.Response(description="Successfull response", schema=VacancyInfoPaginatedResponseSerializer),
        500: openapi.Response(description="Unhandled server error"),
    },
)
@api_view(http_method_names=['GET', 'POST'])
@permission_required(["core.add_vacancy"])
@permission_classes([IsAuthenticated])
@parser_classes([parsers.MultiPartParser])
def vacancies_api_controller(request: Request) -> Response:
    """API controller that returns list of all vacancies."""
    if request.method == 'GET':
        filters_serializer = SearchVacancySerializer(data=request.query_params)
        if filters_serializer.is_valid():
            data = convert_data_from_request_to_dto(
                dto=SearchVacancyDTO, data_from_request=filters_serializer.validated_data
            )
            vacancies = search_vacancies(search_filters=data)
            paginator = APIPaginator(per_page=20)
            result_page = paginator.get_paginated_data(queryset=vacancies, request=request)
            vacancies_info_serializer = VacancyInfoSerializer(result_page, many=True)
            return paginator.paginate(data=vacancies_info_serializer.data)
        else:
            logger.warning(f'The forms have not been validated. Errors: {filters_serializer.errors}')
            return Response(data=filters_serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        add_vacancy_serializer = AddVacancySerializer(data=request.data)
        if add_vacancy_serializer.is_valid():
            vacancy_dto = convert_data_from_request_to_dto(AddVacancyDTO, add_vacancy_serializer.validated_data)
            vacancy_id = create_vacancy(data=vacancy_dto)
        else:
            logger.warning(f'The forms have not been validated. Errors: {add_vacancy_serializer.errors}')
            return Response(data=add_vacancy_serializer.errors, status=HTTP_400_BAD_REQUEST)
        data_message = {"message": "Vacancy created successfully", "vacancy_id": vacancy_id}
        return Response(data=data_message)


@swagger_auto_schema(
    method="GET",
    manual_parameters=[openapi.Parameter(name="vacancy_id", in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER)],
    responses={
        200: openapi.Response(description="Successfully response", schema=VacancyExtendedInfoSerializer(many=True)),
        500: openapi.Response(description="Unhandled server error"),
        404: openapi.Response(description="Resource not found", schema=ErrorSerializer),
    },
)
@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def vacancy_api_controller(request: Request, vacancy_id: int) -> Response:
    """API controller that returns specific vacancy with entered id."""

    try:
        vacancy = get_vacancy_by_id(vacancy_id=vacancy_id)
    except VacancyNotExistsError:
        data = {"message": "Vacancy with provided id doesn't exist."}
        return Response(data=data, status=HTTP_404_NOT_FOUND)
    vacancy_serializer = VacancyExtendedInfoSerializer(vacancy.vacancy)
    return Response(data=vacancy_serializer.data)
