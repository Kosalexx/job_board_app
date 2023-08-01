"""
Custom middleware.
"""

from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Callable

from django.http import HttpResponseBadRequest

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


logger = getLogger(__name__)


class BlockURLMiddleware:
    """Blocks specific URLs (described in BLOCK_URLS)."""

    BLOCK_URLS = ("/block",)

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.path in self.BLOCK_URLS:
            logger.warning('URL blocked by middleware (URL in block list).')
            return HttpResponseBadRequest(content="This url blocked.")

        response = self.get_response(request)
        return response


class TransferRandomMessageMiddleware:
    """Transfers random message to the request."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self._get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        rand_message = "Hello World"
        request.random_message = rand_message
        response = self._get_response(request)

        return response
