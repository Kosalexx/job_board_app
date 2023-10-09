"""
Services and business logic for working with data associated with Company entity in the database.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.models import Address, BusinessArea, City, Company, CompanyProfile, Country, Vacancy
from django.db import transaction
from django.db.models import Count

from .common import change_file_size, replace_file_name_to_uuid

if TYPE_CHECKING:
    from core.business_logic.dto import AddAddressDTO, AddCompanyDTO, AddCompanyProfileDTO


logger = logging.getLogger(__name__)


def create_company(  # pylint: disable=too-many-locals
    company_data: AddCompanyDTO, profile_data: AddCompanyProfileDTO, address_data: AddAddressDTO
) -> None:
    """Records the added company data in the database."""

    with transaction.atomic():
        business_areas: list[str] = company_data.business_area.split("\r\n")
        business_areas_list: list[BusinessArea] = []
        for area in business_areas:
            area = area.lower()
            try:
                area_from_db = BusinessArea.objects.get(name=area)
            except BusinessArea.DoesNotExist as err:
                logger.warning("Business area doesn't exist.", extra={'Business_area': area}, exc_info=err)
                area_from_db = BusinessArea.objects.create(name=area)
                logger.info(
                    'Handled error and successfully created business_area in db.', extra={'Business_area': area}
                )
            business_areas_list.append(area_from_db)
        try:
            address_from_db = Address.objects.select_related('city').get(
                street_name=address_data.street_name,
                home_number=address_data.home_number,
                office_number=address_data.office_number,
                city__country__name=address_data.country,
                city__name=address_data.city,
            )
        except Address.DoesNotExist as err:
            logger.warning(
                "Address doesn't exist.",
                extra={
                    "street_name": address_data.street_name,
                    "home_number": address_data.home_number,
                    "office_number": address_data.office_number,
                    "country_name": address_data.country,
                    "city_name": address_data.city,
                },
                exc_info=err,
            )
            country_from_db = Country.objects.get(name=address_data.country)
            try:
                city_from_db = (
                    City.objects.select_related('country')
                    .filter(country__name=address_data.country)
                    .get(name=address_data.city)
                )
            except City.DoesNotExist as exc:
                logger.warning(
                    "City doesn't exist.",
                    extra={'country': address_data.country, 'city': address_data.city},
                    exc_info=exc,
                )
                city_from_db = City.objects.create(country=country_from_db, name=address_data.city.capitalize())
                logger.info(
                    'Handled error and successfully created city in db.',
                    extra={'country': address_data.country, 'city': address_data.city},
                )
            address_from_db = Address.objects.create(
                street_name=address_data.street_name,
                home_number=address_data.home_number,
                office_number=address_data.office_number,
                city=city_from_db,
            )
            logger.info(
                'Handled error and successfully created address in db.',
                extra={
                    "street_name": address_data.street_name,
                    "home_number": address_data.home_number,
                    "office_number": address_data.office_number,
                    "city": city_from_db,
                },
            )
        created_company = Company.objects.create(name=company_data.name, staff=company_data.staff)
        logger.info(
            'Successfully created country in db.',
            extra={"company_name": company_data.name, "staff": str(company_data.staff)},
        )
        created_company.business_area.set(business_areas_list)
        if profile_data.logo is not None:
            file = replace_file_name_to_uuid(profile_data.logo)
            file = change_file_size(file=file)
        else:
            file = profile_data.logo
        CompanyProfile.objects.create(
            logo=file,
            email=profile_data.email,
            founding_year=profile_data.founding_year,
            description=profile_data.description,
            phone=profile_data.phone,
            website_link=profile_data.website_link,
            linkedin_link=profile_data.linkedin_link,
            github_link=profile_data.github_link,
            twitter_link=profile_data.twitter_link,
            address=address_from_db,
            company=created_company,
        )
        logger.info(
            'Successfully created Company profile in db.',
            extra={
                "company": company_data.name,
                "email": profile_data.email,
                "founding_year": str(profile_data.founding_year),
                "description": profile_data.description,
                "phone": profile_data.phone,
                "website_link": profile_data.website_link,
                "linkedin_link": profile_data.linkedin_link,
                "github_link": profile_data.github_link,
                "twitter_link": profile_data.twitter_link,
            },
        )


def get_companies() -> list[Company]:
    """Gets a list of all companies in the database."""

    companies = Company.objects.annotate(vacancy__count=Count("vacancy__id")).order_by("-vacancy__count")
    logger.info('Successfully got companies list.', extra={'Companies number in db': len(companies)})
    return list(companies)


def get_company_by_id(company_id: int) -> Company:
    """Gets a specific Company data from the database by entered company_id."""

    company: Company = (
        Company.objects.prefetch_related('business_area')
        .annotate(vacancy__count=Count("vacancy__id"))
        .get(pk=company_id)
    )
    logger.info('Successfully got company.', extra={'company_id': str(company_id), 'company_name': company.name})
    return company


def get_company_profile_by_id(company_id: int) -> CompanyProfile:
    """Gets a specific Company_profile data from the database by entered company_id."""

    profile: CompanyProfile = CompanyProfile.objects.select_related('address', 'company').get(pk=company_id)
    logger.info(
        'Successfully got company profile by company_id.',
        extra={'company_id': str(company_id), 'company_name': profile.company.name},
    )
    return profile


def get_vacancies_by_company_id(company_id: int) -> list[Vacancy]:
    """Gets a specific Vacancy data from the database by entered company_id."""

    vacancies = Vacancy.objects.select_related('company').filter(company__id=company_id).order_by("-updated_at")
    logger.info(
        'Successfully got vacancies by company_id.',
        extra={'company_id': str(company_id), 'vacancies number in db': len(vacancies)},
    )
    return list(vacancies)
