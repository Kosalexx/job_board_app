"""
Services and business logic for working with data associated with Vacancy entity in the database.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.dto import VacancyDataDTO
from core.business_logic.exceptions import CompanyNotExistsError, VacancyNotExistsError
from core.business_logic.services.common import replace_file_name_to_uuid
from core.models import City, Company, Country, EmploymentFormat, Level, Response, Tag, Vacancy, WorkFormat
from django.db import transaction
from django.db.models import Count, QuerySet

from .response import get_response_status_by_name

if TYPE_CHECKING:
    from core.business_logic.dto import AddVacancyDTO, ApplyVacancyDTO, SearchVacancyDTO


logger = logging.getLogger(__name__)


def search_vacancies(search_filters: SearchVacancyDTO) -> QuerySet:
    """Gets a list of vacancies from the database by entered filters."""

    vacancies = Vacancy.objects.select_related("level", "company").prefetch_related(
        "tags", "employment_format", "work_format", 'city'
    )

    if search_filters.name:
        vacancies = vacancies.filter(name__icontains=search_filters.name)

    if search_filters.company_name:
        vacancies = vacancies.filter(company__name__icontains=search_filters.company_name)

    if search_filters.level:
        vacancies = vacancies.filter(level__name=search_filters.level)

    if search_filters.experience:
        vacancies = vacancies.filter(experience__icontains=search_filters.experience)

    if search_filters.min_salary:
        vacancies = vacancies.filter(min_salary__gte=search_filters.min_salary)

    if search_filters.max_salary:
        vacancies = vacancies.filter(max_salary__lte=search_filters.max_salary)

    if search_filters.employment_format:
        vacancies = vacancies.filter(employment_format__name__in=search_filters.employment_format)

    if search_filters.work_format:
        vacancies = vacancies.filter(work_format__name__in=search_filters.work_format)

    if search_filters.country:
        inner_country_id = Country.objects.filter(name=search_filters.country)
        vacancies = vacancies.filter(city__country__in=inner_country_id)

    if search_filters.city:
        vacancies = vacancies.filter(city__name=search_filters.city)

    if search_filters.tag:
        vacancies = vacancies.filter(tags__name=search_filters.tag)

    vacancies = vacancies.order_by('-id').distinct()
    position = search_filters.name
    logger.info(
        'The list of vacancies according to the transmitted filters has been successfully received.',
        extra={
            'position': position,
            'company_name': search_filters.company_name,
            'level': search_filters.level,
            'experience': search_filters.experience,
            'min_salary': search_filters.max_salary,
            'max_salary': search_filters.max_salary,
            'employment_format': search_filters.employment_format,
            'work_format': search_filters.work_format,
            'country': search_filters.country,
            'city': search_filters.city,
            'tag': search_filters.tag,
        },
    )

    return vacancies


def create_vacancy(data: AddVacancyDTO) -> int:  # pylint: disable=too-many-locals
    """Records the added Vacancy data in the database."""

    with transaction.atomic():
        tags: list[str] = data.tags.split("\r\n")
        tags_list: list[Tag] = []
        for tag in tags:
            try:
                tag_from_db = Tag.objects.get(name=tag.lower())
            except Tag.DoesNotExist as err:
                logger.warning("Tag doesn't exist.", extra={'Tag': tag}, exc_info=err)
                tag_from_db = Tag.objects.create(name=tag.lower())
                logger.info('Handled error and successfully created tag in db.', extra={'tag': tag})
            tags_list.append(tag_from_db)
        try:
            company = Company.objects.get(name=data.company_name)
        except Company.DoesNotExist as exc:
            logger.warning("Company doesn't exists.", extra={'company': data.company_name}, exc_info=exc)
            raise CompanyNotExistsError from exc

        cities: list[str] = data.city.split('\r\n')
        city_list: list[City] = []
        for city in cities:
            try:
                city_from_db = (
                    City.objects.select_related('country')
                    .filter(country__name=data.country)
                    .get(name=city.capitalize())
                )
            except City.DoesNotExist as err:
                logger.warning("City doesn't exists.", extra={'city': city}, exc_info=err)
                city_from_db = City.objects.create(
                    name=city.capitalize(), country=Country.objects.get(name=data.country)
                )
                logger.info('Handled error and successfully created city in db.', extra={'city': city})
            city_list.append(city_from_db)
        employment_formats_list: list[EmploymentFormat] = [
            EmploymentFormat.objects.get(name=employ_format) for employ_format in data.employment_format
        ]
        work_formats_list: list[WorkFormat] = [WorkFormat.objects.get(name=work_form) for work_form in data.work_format]
        if data.attachment is not None:
            file = replace_file_name_to_uuid(data.attachment)
        else:
            file = data.attachment
        created_vacancy = Vacancy.objects.create(
            name=data.name,
            level=Level.objects.get(name=data.level),
            company=company,
            experience=data.experience,
            min_salary=data.min_salary,
            max_salary=data.max_salary,
            description=data.description,
            attachment=file,
        )
        logger.info(
            'Successfully created vacancy in db.',
            extra={
                "vacancy_name": data.name,
                "level": data.level,
                "company": data.company_name,
                "experience": data.experience,
                "min_salary": data.min_salary,
                "max_salary": data.max_salary,
                "description": data.description,
                "attachment": file,
            },
        )
        created_vacancy.employment_format.set(employment_formats_list)
        created_vacancy.work_format.set(work_formats_list)
        created_vacancy.tags.set(tags_list)
        created_vacancy.city.set(city_list)
        logger.info(  # pylint: disable=logging-fstring-interpolation
            f'Related with the vacancy "{data.name}" data about Employment formats, work formats, tags,'
            f'and cities has been added to the database.',
            extra={
                "employment_format": employment_formats_list,
                "work_format": work_formats_list,
                "tags": tags_list,
                "cities": city_list,
            },
        )
        vacancy_id: int = created_vacancy.pk
        return vacancy_id


def get_vacancy_by_id(
    vacancy_id: int,
) -> VacancyDataDTO:
    """Gets a specific Vacancy data from the database by entered vacancy_id."""

    try:
        vacancy = (
            Vacancy.objects.select_related("level", "company")
            .prefetch_related("tags", "employment_format", "work_format", 'city')
            .annotate(num_work_format=Count("work_format", distinct=True))
            .get(pk=vacancy_id)
        )
        tags = vacancy.tags.all()
        employment_format = vacancy.employment_format.all()
        work_format = vacancy.work_format.all()
        city = vacancy.city.all()
        logger.info(
            'Successfully got vacancy data.', extra={'vacancy_id': str(vacancy_id), 'vacancy_name': vacancy.name}
        )
        result = VacancyDataDTO(
            vacancy=vacancy,
            tags=list(tags),
            employment_format=list(employment_format),
            work_format=list(work_format),
            city=list(city),
        )
    except Vacancy.DoesNotExist:
        raise VacancyNotExistsError
    return result


def apply_to_vacancy(data: ApplyVacancyDTO) -> None:
    """Creates job response."""
    response_status = get_response_status_by_name('New')
    Response.objects.create(
        user=data.user, vacancy=data.vacancy, cover_note=data.cover_note, cv=data.cv, response_status=response_status
    )
