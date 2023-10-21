from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.dto import SearchVacancyDTO
from core.business_logic.services import search_vacancies
from core.presentation.api_v1.serializers import SearchVacancySerializer, VacancyInfoSerializer
from core.presentation.common.converters import convert_data_from_request_to_dto
from rest_framework.decorators import api_view
from rest_framework.response import Response

if TYPE_CHECKING:
    from rest_framework.request import Request


@api_view(http_method_names=['GET'])
def get_vacancies_api_controller(request: Request) -> Response:
    filters_serializer = SearchVacancySerializer(data=request.query_params)
    if filters_serializer.is_valid():
        data = convert_data_from_request_to_dto(
            dto=SearchVacancyDTO, data_from_request=filters_serializer.validated_data
        )
        vacancies = search_vacancies(search_filters=data)
        vacancies_info_serializer = VacancyInfoSerializer(vacancies, many=True)
        return Response(data=vacancies_info_serializer.data)
    return Response(data={"message": "Invalid serializer"})
