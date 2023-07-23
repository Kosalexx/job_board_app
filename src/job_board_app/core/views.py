"""
Views (controllers) for job_board_app.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from django.http import (
    Http404,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import AddCompanyForm, AddReviewForm, AddVacancyForm
from .services import (
    Company,
    CompanyStorage,
    Review,
    ReviewStorage,
    Vacancy,
    VacancyStorage,
)

if TYPE_CHECKING:
    from django.http import HttpRequest


company_storage = CompanyStorage()
vacancy_storage = VacancyStorage(company_storage=company_storage)
review_storage = ReviewStorage(company_storage=company_storage)


@require_http_methods(request_method_list=['GET'])
def index_controller(request: HttpRequest) -> HttpResponse:
    """Controller for index(main) page."""
    vacancies = vacancy_storage.get_all_vacancies()
    context = {"vacancies": vacancies}
    return render(request=request, template_name="index.html", context=context)


@require_http_methods(request_method_list=['GET', 'POST'])
def add_company_controller(request: HttpRequest) -> HttpResponse:
    """Controller for adding a new company."""
    if request.method == 'GET':
        form = AddCompanyForm()
        context = {'form': form}
        return render(request=request, template_name="add_company.html", context=context)
    if request.method == 'POST':
        form = AddCompanyForm(data=request.POST)
        if form.is_valid():
            name: str = form.cleaned_data['name']
            employees_number: int = form.cleaned_data['employees_number']
            company = Company(name=name, employees_number=employees_number)
            company_storage.add_company(company_to_add=company)
            return HttpResponseRedirect(redirect_to=reverse("company-list"))
    return HttpResponseBadRequest("Incorrect HTTP method.")


@require_http_methods(request_method_list=['GET'])
def companies_list_controller(request: HttpRequest) -> HttpResponse:
    """Controller for the page with a list of all companies."""
    companies = company_storage.get_all_companies()
    context = {'companies': companies}
    return render(request=request, template_name="company_list.html", context=context)


@require_http_methods(request_method_list=['GET', 'POST'])
def add_vacancy_controller(request: HttpRequest) -> HttpResponse:
    """Controller for adding a new vacancy."""
    if request.method == "GET":
        form = AddVacancyForm()
        context = {"form": form}
        return render(request=request, template_name="add_vacancy.html", context=context)
    if request.method == 'POST':
        form = AddVacancyForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            company_name = form.cleaned_data['company_name']
            experience = form.cleaned_data['experience']
            level = form.cleaned_data['level']
            min_salary = form.cleaned_data['min_salary']
            max_salary = form.cleaned_data['max_salary']
            vacancy = Vacancy(
                name=name,
                company=company_storage.get_company_by_name(company_name),
                level=level,
                experience=experience,
                min_salary=min_salary,
                max_salary=max_salary,
            )
            vacancy_storage.add_vacancy(vacancy_to_add=vacancy)
            return HttpResponseRedirect(redirect_to=reverse("index"))
    return HttpResponseBadRequest("Incorrect HTTP method.")


@require_http_methods(request_method_list=['GET'])
def get_vacancy_controller(request: HttpRequest, vacancy_id: int) -> HttpResponse:
    """Controller for specific vacancy."""
    vacancy = vacancy_storage.get_vacancy_by_id(vacancy_id=vacancy_id)
    if vacancy:
        context = {"vacancy": vacancy}
        return render(request=request, template_name="specific_vacancy.html", context=context)
    raise Http404("Page not found.")


@require_http_methods(request_method_list=['GET'])
def get_company_controller(request: HttpRequest, company_id: int) -> HttpResponse:
    """Controller for specific company."""
    company = company_storage.get_company_by_id(company_id=company_id)
    if company:
        vacancies = vacancy_storage.get_vacancy_by_company(company.name)
        reviews = review_storage.get_all_reviews_by_company_id(company_id=company_id)
        context = {"company": company, "vacancies": vacancies, "reviews": reviews}
        return render(request=request, template_name="specific_company.html", context=context)
    raise Http404("Page not found.")


@require_http_methods(request_method_list=['GET', 'POST'])
def get_review_controller(request: HttpRequest, company_id: int) -> HttpResponse:
    """Controller for creating a new review."""
    if request.method == "GET":
        form = AddReviewForm()
        company = company_storage.get_company_by_id(company_id=company_id)
        context = {"company": company, "form": form}
        return render(request=request, template_name="company_review.html", context=context)

    if request.method == "POST":
        form = AddReviewForm(data=request.POST)
        if form.is_valid():
            company = company_storage.get_company_by_id(company_id=company_id)
            user_name = form.cleaned_data['user_name']
            review_text = form.cleaned_data['review_text']
            creation_datetime = str(datetime.now())
            update_datetime = str(datetime.now())
            review = Review(
                user_name=user_name,
                company=company,
                text=review_text,
                creation_datetime=creation_datetime,
                update_datetime=update_datetime,
            )
            review_storage.add_review(review_to_add=review)
            return HttpResponseRedirect(redirect_to=reverse("specific_company", args=(company_id,)))
    return HttpResponseBadRequest("Incorrect HTTP method.")


@require_http_methods(request_method_list=['GET', 'POST'])
def get_user_info(request: HttpRequest) -> HttpResponse:
    """Controller for getting, adding, and updating user info."""
    return render(request=request, template_name='user_profile.html')
