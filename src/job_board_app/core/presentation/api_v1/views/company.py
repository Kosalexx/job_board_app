from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.services import get_companies
from core.presentation.api_v1.serializers import CompaniesListSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

if TYPE_CHECKING:
    from rest_framework.request import Request


@api_view(http_method_names=['GET'])
def get_companies_api_controller(request: Request) -> Response:
    companies = get_companies()
    companies_serializer = CompaniesListSerializer(companies, many=True)
    return Response(data=companies_serializer.data)
