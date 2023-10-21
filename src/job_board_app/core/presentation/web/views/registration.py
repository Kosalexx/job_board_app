"""
Views (controllers) for job_board_app that related with Vacancy entity.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.dto import RegistrationDTO
from core.business_logic.exceptions import (
    ConfirmationCodeExpiredError,
    ConfirmationCodeNotExistError,
    UserAlreadyExistsError,
)
from core.business_logic.services import confirm_user_registration, create_user, get_groups
from core.presentation.common.converters import convert_data_from_request_to_dto
from core.presentation.web.forms import RegistrationForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest


ROLES = get_groups()


@require_http_methods(['GET', 'POST'])
def registration_controller(request: HttpRequest) -> HttpResponse:
    """Controller for registration(sign in) page."""

    if request.method == 'GET':
        form = RegistrationForm(ROLES)
        context_1 = {'form': form}
        return render(request=request, template_name='sign-up.html', context=context_1)
    if request.method == 'POST':
        form = RegistrationForm(ROLES, request.POST)
        if form.is_valid():
            received_data = convert_data_from_request_to_dto(dto=RegistrationDTO, data_from_request=form.cleaned_data)
            try:
                create_user(data=received_data)
                context_2 = {"new_email": received_data.email}
                return render(request=request, template_name="email_changed.html", context=context_2)
            except UserAlreadyExistsError:
                context = {
                    "title": "Sign up",
                    "form": form,
                    "err_message": "The user with the entered username or email already exists... Please try again.",
                }
                return render(request=request, template_name="sign-up.html", context=context)

        context_3 = {"form": form}
        return render(request=request, template_name='sign-up.html', context=context_3)
    return HttpResponseBadRequest("Incorrect HTTP method.")


@require_http_methods(['GET'])
def registration_confirmation(request: HttpRequest) -> HttpResponse:
    """Controller for registration confirmation page."""

    received_code = request.GET["code"]
    try:
        confirm_user_registration(confirmation_code=received_code)
    except ConfirmationCodeNotExistError:
        return HttpResponseBadRequest(content="Invalid confirmation code")
    except ConfirmationCodeExpiredError:
        return HttpResponseBadRequest(
            content="The confirmation code is expired. The new confirmation link has been sent to your email."
            "Please follow this link to confirm your registration."
        )
    return redirect(to="login")
