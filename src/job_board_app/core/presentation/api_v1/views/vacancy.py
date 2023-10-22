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
    AddVacancySerializer,
    SearchVacancySerializer,
    VacancyExtendedInfoSerializer,
    VacancyInfoSerializer,
)
from core.presentation.common.converters import convert_data_from_request_to_dto
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

if TYPE_CHECKING:
    from rest_framework.request import Request


logger = getLogger(__name__)


@api_view(http_method_names=['GET', 'POST'])
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


@api_view(http_method_names=['GET'])
def vacancy_api_controller(request: Request, vacancy_id: int) -> Response:
    """API controller that returns specific vacancy with entered id."""

    try:
        vacancy = get_vacancy_by_id(vacancy_id=vacancy_id)
    except VacancyNotExistsError:
        data = {"message": "Vacancy with provided id doesn't exist."}
        return Response(data=data, status=HTTP_404_NOT_FOUND)
    vacancy_serializer = VacancyExtendedInfoSerializer(vacancy.vacancy)
    return Response(data=vacancy_serializer.data)
