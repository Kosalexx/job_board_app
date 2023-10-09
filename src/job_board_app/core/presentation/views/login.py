"""
Views (controllers) for job_board_app that related with login logic.
"""
from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from core.business_logic.dto import LoginDTO
from core.business_logic.exceptions import InvalidAuthCredentialsError
from core.business_logic.services import authenticate_user
from core.presentation.converters import convert_data_from_form_to_dto
from core.presentation.forms import LoginForm
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest


logger = getLogger(__name__)


@require_http_methods(['GET', 'POST'])
def login_controller(request: HttpRequest) -> HttpResponse:
    """Controller for login and authentication on the server."""
    if request.method == 'GET':
        form = LoginForm()
        context = {'form': form}
        return render(request=request, template_name='login.html', context=context)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = convert_data_from_form_to_dto(dto=LoginDTO, data_from_form=form.cleaned_data)

            try:
                user = authenticate_user(data=data)
            except InvalidAuthCredentialsError as err:
                logger.error(
                    'Invalid entered user credentials',
                    extra={'username': data.username, 'password': data.password},
                    exc_info=err,
                )
                return HttpResponseBadRequest(content='Invalid credentials.')
            login(request=request, user=user)
            return redirect(to='index')

        context = {"form": form}
        return render(request=request, template_name='login.html', context=context)

    return HttpResponseBadRequest("Incorrect HTTP method.")
