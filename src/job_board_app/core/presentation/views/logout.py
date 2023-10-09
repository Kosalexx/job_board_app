"""
Views (controllers) for job_board_app that related with login logic.
"""
from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest


logger = getLogger(__name__)


@require_http_methods(['GET'])
def logout_controller(request: HttpRequest) -> HttpResponse:
    """Controller for logout on the server."""
    if request.method == 'GET':
        username = request.user.username
        logout(request=request)
        logger.info('Successful logout.', extra={'user': username})
        return redirect(to='index')
    return HttpResponseBadRequest("Incorrect HTTP method.")
