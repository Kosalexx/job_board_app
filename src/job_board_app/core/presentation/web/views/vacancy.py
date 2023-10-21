"""
Views (controllers) for job_board_app that related with Vacancy entity.
"""

from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from core.business_logic.dto import AddVacancyDTO, ApplyVacancyDTO, SearchVacancyDTO
from core.business_logic.exceptions import CompanyNotExistsError
from core.business_logic.services import (
    apply_to_vacancy,
    create_vacancy,
    get_countries,
    get_employment_formats,
    get_levels,
    get_vacancy_by_id,
    get_work_formats,
    search_vacancies,
)
from core.presentation.common.converters import convert_data_from_request_to_dto
from core.presentation.web.forms import AddVacancyForm, ApplyVacancyForm, SearchVacancyForm
from core.presentation.web.pagination import CustomPagination, PageNotExists
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest


logger = getLogger(__name__)

COUNTRIES: list[tuple[str, str]] = get_countries()
WORK_FORMATS: list[tuple[str, str]] = get_work_formats()
EMPLOYMENT_FORMATS: list[tuple[str, str]] = get_employment_formats()
LEVELS: list[tuple[str, str]] = get_levels()


@require_http_methods(request_method_list=["GET"])
def index_controller(request: HttpRequest) -> HttpResponse:
    """Controller for index(main) page."""
    filters_form = SearchVacancyForm(
        levels=[('', 'All')] + LEVELS,
        employment_formats=EMPLOYMENT_FORMATS,
        work_formats=WORK_FORMATS,
        countries=[('', 'All')] + COUNTRIES,
        data=request.GET,
    )
    logger.info('index_page_log')
    if filters_form.is_valid():
        search_filters = convert_data_from_request_to_dto(SearchVacancyDTO, filters_form.cleaned_data)
        vacancies = search_vacancies(search_filters=search_filters)
        form = SearchVacancyForm(
            levels=[('', 'All')] + LEVELS,
            employment_formats=EMPLOYMENT_FORMATS,
            work_formats=WORK_FORMATS,
            countries=[('', 'All')] + COUNTRIES,
            data=request.GET,
        )
        page_number = request.GET.get("page", 1)
        paginator = CustomPagination(per_page=20)
        try:
            vacancies_paginated = paginator.paginate(data=vacancies, page_number=page_number)
        except PageNotExists:
            return HttpResponseBadRequest("Page with provided number doesn't exist.")
        context = {"vacancies": vacancies_paginated.data, "form": form}
        logger.info(
            "Successfully rendered index page by entered filters.",
            extra={'Vacancies number': len(vacancies), "filter_data": filters_form.changed_data},
        )
    else:
        context = {"form": filters_form}
    return render(request=request, template_name="index.html", context=context)


@permission_required(["core.add_vacancy"])
@transaction.non_atomic_requests
@require_http_methods(request_method_list=["GET", "POST"])
def add_vacancy_controller(request: HttpRequest) -> HttpResponse:
    """Controller for adding a new vacancy."""
    if request.method == "GET":
        form = AddVacancyForm(
            levels=LEVELS, employment_formats=EMPLOYMENT_FORMATS, work_formats=WORK_FORMATS, countries=COUNTRIES
        )
        context = {"form": form}
        logger.info("Successfully rendered form for adding vacancy.")
        return render(request=request, template_name="add_vacancy.html", context=context)

    if request.method == 'POST':
        form = AddVacancyForm(
            levels=LEVELS,
            employment_formats=EMPLOYMENT_FORMATS,
            work_formats=WORK_FORMATS,
            countries=COUNTRIES,
            data=request.POST,
            files=request.FILES,
        )
        if form.is_valid():
            data = convert_data_from_request_to_dto(AddVacancyDTO, form.cleaned_data)
            logger.info(
                'Form have been validated. The vacancy will be added to the database.',
                extra={
                    'vacancy_name': data.name,
                },
            )
            try:
                create_vacancy(data=data)
            except CompanyNotExistsError as err:
                logger.error(  # pylint: disable=logging-fstring-interpolation
                    f"Company '{data.company_name}' doesn't exist in the database.",
                    extra={'company_name': data.company_name},
                    exc_info=err,
                )
                return HttpResponseBadRequest(content="Provided company doesn't exist.")
        else:
            logger.warning('The forms have not been validated.')
            context = {"form": form}
            return render(request=request, template_name="add_vacancy.html", context=context)

        return HttpResponseRedirect(redirect_to=reverse("index"))
    return HttpResponseBadRequest("Incorrect HTTP method.")


@require_http_methods(request_method_list=['GET'])
def get_vacancy_controller(request: HttpRequest, vacancy_id: int) -> HttpResponse:
    """Controller for specific vacancy."""
    vacancy_dto = get_vacancy_by_id(vacancy_id=vacancy_id)
    vacancy = vacancy_dto.vacancy
    tags = vacancy_dto.tags
    employment_format = vacancy_dto.employment_format
    work_format = vacancy_dto.work_format
    city = vacancy_dto.city
    context = {
        "vacancy": vacancy,
        "tags": tags,
        "employment_format": employment_format,
        "work_format": work_format,
        "city": city,
    }
    logger.info(  # pylint: disable=logging-fstring-interpolation
        f'Successfully rendered template(page) of vacancy {vacancy.name}.', extra={'vacancy_name': vacancy.name}
    )
    return render(request=request, template_name="get_vacancy.html", context=context)


@login_required
@permission_required(['core.apply_to_vacancy'])
@require_http_methods(request_method_list=['GET', 'POST'])
def apply_vacancy_controller(request: HttpRequest, vacancy_id: int) -> HttpResponse:
    """Controller for apply to vacancy logic."""
    if request.method == 'GET':
        form = ApplyVacancyForm()
        context = {'form': form, "vacancy_id": vacancy_id}
        return render(request=request, template_name='apply_vacancy.html', context=context)
    else:
        form = ApplyVacancyForm(request.POST, files=request.FILES)
        if form.is_valid():
            data = convert_data_from_request_to_dto(ApplyVacancyDTO, form.cleaned_data)
            data.user = request.user
            data.vacancy = get_vacancy_by_id(vacancy_id=vacancy_id).vacancy
            apply_to_vacancy(data=data)
        else:
            logger.warning('The forms have not been validated.')
            context = {'form': form, "vacancy_id": vacancy_id}
            return render(request=request, template_name="apply_vacancy.html", context=context)
        return redirect(to='post-apply')


@login_required
@permission_required(['core.apply_to_vacancy'])
@require_http_methods(request_method_list=['GET', 'POST'])
def successfully_apply_controller(request: HttpRequest) -> HttpResponse:
    """Controller for successfully apply."""
    return render(request=request, template_name='apply_success.html')
