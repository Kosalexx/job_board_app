from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rest_framework.pagination import PageNumberPagination

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from rest_framework.request import Request
    from rest_framework.response import Response


class APIPaginator:
    """Custom API paginator."""

    def __init__(self, per_page: int) -> None:
        self._per_page = per_page
        self._paginator_class = PageNumberPagination()
        self._paginator_class.page_size = self._per_page

    def get_paginated_data(self, queryset: QuerySet, request: Request) -> list | None:
        """Gets paginated data from queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view."""
        result: list | None = self._paginator_class.paginate_queryset(queryset=queryset, request=request)
        return result

    def paginate(self, data: Any) -> Response:
        """Creates paginated response."""
        return self._paginator_class.get_paginated_response(data=data)
