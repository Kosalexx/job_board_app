"""
Views (controllers) for job_board_app that related with Vacancy entity.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.dto import AddVacancyDTO, SearchVacancyDTO
from core.business_logic.exceptions import CompanyNotExists
from core.business_logic.services import create_vacancy, get_vacancy_by_id, search_vacancies
from core.presentation.converters import convert_data_from_form_to_dto
from core.presentation.forms import AddVacancyForm, SearchVacancyForm
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest


logger = logging.getLogger(__name__)


@require_http_methods(request_method_list=["GET"])
def index_controller(request: HttpRequest) -> HttpResponse:
    """Controller for index(main) page."""
    filters_form = SearchVacancyForm(request.GET)
    logger.info('index_page_log')
    if filters_form.is_valid():
        search_filters = convert_data_from_form_to_dto(SearchVacancyDTO, filters_form.cleaned_data)

        vacancies = search_vacancies(search_filters=search_filters)

        form = SearchVacancyForm()
        context = {"vacancies": vacancies, "form": form}
    else:
        context = {"form": filters_form}
    return render(request=request, template_name="index.html", context=context)


@transaction.non_atomic_requests
@require_http_methods(request_method_list=["GET", "POST"])
def add_vacancy_controller(request: HttpRequest) -> HttpResponse:
    """Controller for adding a new vacancy."""
    if request.method == "GET":
        form = AddVacancyForm()
        context = {"form": form}
        return render(request=request, template_name="add_vacancy.html", context=context)

    if request.method == 'POST':
        form = AddVacancyForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            data = convert_data_from_form_to_dto(AddVacancyDTO, form.cleaned_data)
            try:
                create_vacancy(data=data)
            except CompanyNotExists:
                return HttpResponseBadRequest(content="Provided company doesn't exist.")
        else:
            context = {"form": form}
            return render(request=request, template_name="add_vacancy.html", context=context)

        return HttpResponseRedirect(redirect_to=reverse("index"))
    return HttpResponseBadRequest("Incorrect HTTP method.")


@require_http_methods(request_method_list=['GET'])
def get_vacancy_controller(request: HttpRequest, vacancy_id: int) -> HttpResponse:
    """Controller for specific vacancy."""
    vacancy, tags, employment_format, work_format, city = get_vacancy_by_id(vacancy_id=vacancy_id)
    context = {
        "vacancy": vacancy,
        "tags": tags,
        "employment_format": employment_format,
        "work_format": work_format,
        "city": city,
    }
    return render(request=request, template_name="get_vacancy.html", context=context)
