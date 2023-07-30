"""
Views (controllers) for job_board_app that related with Vacancy entity.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.dto import RegistrationDTO
from core.business_logic.services import create_user
from core.presentation.converters import convert_data_from_form_to_dto
from core.presentation.forms import RegistrationForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest


@require_http_methods(['GET', 'POST'])
def registration_controller(request: HttpRequest) -> HttpResponse:
    """Controller for registration(sign in) page."""

    if request.method == 'GET':
        form = RegistrationForm()
        context = {'form': form}
        return render(request=request, template_name='registration.html', context=context)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = convert_data_from_form_to_dto(dto=RegistrationDTO, data_from_form=form.cleaned_data)
            create_user(data=data)
            return redirect(to="index")

        context = {"form": form}
        return render(request=request, template_name='registration.html', context=context)
    return HttpResponseBadRequest("Incorrect HTTP method.")
