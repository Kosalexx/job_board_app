"""
Views (controllers) for job_board_app.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .services import Company, CompanyStorage, Vacancy, VacancyStorage

if TYPE_CHECKING:
    from django.http import HttpRequest


company_storage = CompanyStorage()
vacancy_storage = VacancyStorage(company_storage=company_storage)


def index_controller(request: HttpRequest) -> HttpResponse:
    """Controller for index(main) page."""
    vacancies = vacancy_storage.get_all_vacancies()
    context = {"vacancies": vacancies}
    return render(request=request, template_name="index.html", context=context)


def add_company_controller(request: HttpRequest) -> HttpResponse | None:
    """Controller for adding a new company."""
    if request.method == 'GET':
        return render(request=request, template_name="add_company.html")
    if request.method == 'POST':
        name = request.POST['name']
        employees_number = request.POST['employees_number']
        company = Company(name=name, employees_number=employees_number)
        company_storage.add_company(company_to_add=company)
        return HttpResponseRedirect(redirect_to="/company/")
    return None


def companies_list_controller(request: HttpRequest) -> HttpResponse:
    """Controller for the page with a list of all companies."""
    companies = company_storage.get_all_companies()
    context = {'companies': companies}
    return render(request=request, template_name="company_list.html", context=context)


def add_vacancy_controller(request: HttpRequest) -> HttpResponse | None:
    """Controller for adding a new vacancy."""
    if request.method == "GET":
        return render(request=request, template_name="add_vacancy.html")
    if request.method == 'POST':
        name = request.POST["name"]
        company_name = request.POST["company_name"]
        level = request.POST["level"]
        experience = request.POST["experience"]
        min_salary = request.POST["min_salary"]
        max_salary = request.POST["max_salary"]

        if min_salary == "":
            min_salary = None
        else:
            min_salary = int(min_salary)
        if max_salary == "":
            max_salary = None
        else:
            max_salary = int(max_salary)
        vacancy = Vacancy(
            name=name,
            company=company_name,
            level=level,
            experience=experience,
            min_salary=min_salary,
            max_salary=max_salary,
        )
        vacancy_storage.add_vacancy(vacancy_to_add=vacancy)
        return HttpResponseRedirect(redirect_to="/")
    return None
