"""
Views (controllers) for job_board_app that related with Company entity.
"""


from __future__ import annotations

from typing import TYPE_CHECKING

from core.business_logic.dto import AddAddressDTO, AddCompanyDTO, AddCompanyProfileDTO
from core.business_logic.services import (
    create_company,
    get_companies,
    get_company_by_id,
    get_company_profile_by_id,
    get_vacancies_by_company_id,
)
from core.presentation.converters import convert_data_from_form_to_dto
from core.presentation.forms import AddAddressFrom, AddCompanyForm, CompanyProfileForm
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest


@require_http_methods(request_method_list=['GET', 'POST'])
def add_company_controller(request: HttpRequest) -> HttpResponse:
    """Controller for adding a new company."""
    if request.method == "GET":
        company_form = AddCompanyForm(prefix='company')
        profile_form = CompanyProfileForm(prefix='profile')
        address_form = AddAddressFrom(prefix='address')
        context = {"company_form": company_form, "profile_form": profile_form, "address_form": address_form}
        return render(request=request, template_name="add_company.html", context=context)

    if request.method == "POST":
        company_form = AddCompanyForm(request.POST, prefix='company')
        profile_form = CompanyProfileForm(request.POST, request.FILES, prefix='profile')
        address_form = AddAddressFrom(request.POST, prefix='address')
        if company_form.is_valid() and profile_form.is_valid() and address_form.is_valid():
            company_data = convert_data_from_form_to_dto(AddCompanyDTO, company_form.cleaned_data)
            profile_data = convert_data_from_form_to_dto(AddCompanyProfileDTO, profile_form.cleaned_data)
            address_data = convert_data_from_form_to_dto(AddAddressDTO, address_form.cleaned_data)
            create_company(company_data=company_data, profile_data=profile_data, address_data=address_data)
        else:
            context = {"company_form": company_form, "profile_form": profile_form, "address_form": address_form}
            return render(request=request, template_name="add_company.html", context=context)
        return HttpResponseRedirect(redirect_to=reverse("company-list"))
    return HttpResponseBadRequest("Incorrect HTTP method.")


@require_http_methods(request_method_list=['GET'])
def companies_list_controller(request: HttpRequest) -> HttpResponse:
    """Controller for the page with a list of all companies."""
    companies = get_companies()
    context = {"companies": companies}
    return render(request=request, template_name="company_list.html", context=context)


@require_http_methods(request_method_list=['GET'])
def get_company_controller(request: HttpRequest, company_id: int) -> HttpResponse:
    """Controller for specific company."""
    company = get_company_by_id(company_id=company_id)
    profile = get_company_profile_by_id(company_id=company_id)
    vacancies = get_vacancies_by_company_id(company_id=company_id)
    context = {"company": company, "profile": profile, "vacancies": vacancies}
    return render(request=request, template_name="get_company.html", context=context)
