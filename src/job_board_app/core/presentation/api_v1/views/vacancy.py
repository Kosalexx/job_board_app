"""
API Views (controllers) for job_board_app that related with vacancy logic.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.dto import SearchVacancyDTO
from core.business_logic.services import get_vacancy_by_id, search_vacancies
from core.presentation.api_v1.pagination import APIPaginator
from core.presentation.api_v1.serializers import (
    SearchVacancySerializer,
    VacancyExtendedInfoSerializer,
    VacancyInfoSerializer,
)
from core.presentation.common.converters import convert_data_from_request_to_dto
from rest_framework.decorators import api_view
from rest_framework.response import Response

if TYPE_CHECKING:
    from rest_framework.request import Request


@api_view(http_method_names=['GET'])
def get_vacancies_api_controller(request: Request) -> Response:
    """API controller that returns list of all vacancies."""
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
    return Response(data={"message": "Invalid serializer"})


@api_view(http_method_names=['GET'])
def get_vacancy_api_controller(request: Request, vacancy_id: int) -> Response:
    """API controller that returns specific company with entered id."""

    vacancy = get_vacancy_by_id(vacancy_id=vacancy_id)
    vacancy_serializer = VacancyExtendedInfoSerializer(vacancy.vacancy)
    return Response(data=vacancy_serializer.data)
