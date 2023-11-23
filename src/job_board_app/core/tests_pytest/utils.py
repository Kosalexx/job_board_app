import re
import sys
import tempfile
from io import BytesIO

from core.models import (
    Address,
    BusinessArea,
    City,
    Company,
    CompanyProfile,
    Country,
    EmploymentFormat,
    Level,
    Tag,
    Vacancy,
    WorkFormat,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, Group
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from PIL import Image


def get_test_image() -> InMemoryUploadedFile:
    """
    Creates Image for further use in tests.

    :rtype: InMemoryUploadedFile
    :return: fake Image object that can be used as a company logo
    """

    output = BytesIO()
    image = Image.new('RGB', (100, 100))
    image.save(output, format='PNG', quality=100)
    return InMemoryUploadedFile(
        file=output, field_name=None, name="test.png", content_type="image/png", size=10, charset=None
    )


def get_test_file_bytes() -> BytesIO:
    """
    Creates Bytes fil for further use in tests.

    :rtype: BytesIO
    :return: fake BytesIO file object that can be used as a
    """
    output = BytesIO()
    image = Image.new("RGB", (100, 100))
    image.save(output, format="PNG", quality=100)
    return output


def get_test_pdf() -> InMemoryUploadedFile:
    """
    Creates PDF file for further use in tests.

    :rtype: InMemoryUploadedFile
    :return: fake PDF file object that can be used as a company logo
    """
    with tempfile.NamedTemporaryFile(mode='w+b', suffix='.pdf') as file:
        output = BytesIO(file.read())
        return InMemoryUploadedFile(
            file=output,
            field_name=None,
            name="test.pdf",
            content_type="application/pdf",
            size=sys.getsizeof(file),
            charset=None,
        )


def create_test_company_in_db(company_name: str, test_file: InMemoryUploadedFile) -> Company:
    """
    Creates test company with passed company name and file object.

    :param company_name: name of created company
    :type company_name: str
    :param test_file: File object that will be used as a company logo
    :type test_file: InMemoryUploadedFile

    :rtype: Company
    :return: created in the database Company object
    """
    with transaction.atomic():
        new_company: Company = Company.objects.create(name=company_name, staff=100)

        business_areas_list = []
        for i in range(3):
            new_area = BusinessArea.objects.create(name=f'test_area_{i}_{company_name}')
            business_areas_list.append(new_area)
        new_company.business_area.set(business_areas_list)

        try:
            country = Country.objects.get(name='Belarus')
        except Country.DoesNotExist:
            country = Country.objects.create(name='Belarus')

        new_city = City.objects.create(name=f'Test_city_{company_name}', country=country)
        address = Address.objects.create(street_name='Test_street_name', home_number=1, office_number=1, city=new_city)

        CompanyProfile.objects.create(
            logo=test_file,
            email=f'{company_name}@gmail.com',
            founding_year=2000,
            description='test_description',
            phone='+375256666666',
            website_link=f'{company_name}.com',
            linkedin_link=None,
            github_link=None,
            twitter_link=None,
            address=address,
            company=new_company,
        )
        return new_company


def create_test_vacancy_in_db(
    vacancy_name: str,
    company: Company,
    attachment_file: InMemoryUploadedFile,
    level: str = 'Junior',
    experience: str | None = '0 years',
    min_salary: int | None = None,
    max_salary: int | None = None,
    description: str | None = None,
    tags: str | None = 'tag1 tag2',
    country: str = 'Belarus',
    cities: str = 'Minsk Brest',
    employment_formats: list = ['B2B', 'Employment contract'],  # noqa: B006
    work_formats: list = ['Remote work', 'Hybrid'],  # noqa: B006
) -> Vacancy:
    """
    Creates test vacancy with passed data and default values.

    :param vacancy_name: name of created vacancy
    :type vacancy_name: str
    :param company: Company object
    :type company: Company
    :param attachment_file: File object that will be used as a company logo
    :type test_file: InMemoryUploadedFile
    :param level: required level of candidate. Default = 'Junior'
    :type level: str
    :param experience: required experience of candidate. Default = '0 years'
    :type experience: str | None
    :param min_salary: minimum salary bracket. Default = None
    :type min_salary: int | None
    :param max_salary: maximum salary bracket. Default = None
    :type max_salary: int | None
    :param description: vacancy description. Default = 'None'
    :type description: str | None
    :param country: created vacancy country. Default = 'Belarus'
    :type country: str
    :param city: created vacancy possible cities (' '(space) separated). Default = 'Minsk Brest'
    :type city: str
    :param tags: created vacancy related tags (' '(space) separated). Default = 'tag1 tag2'
    :type tags: str | None
    :param employment_format: possible employment formats. Default = ['B2B', 'Employment contract']
    :type employment_format: list
    :param work_format: possible work formats. Default = ['Remote work', 'Hybrid']
    :type work_format: list


    :rtype: Vacancy
    :return: created in the database Vacancy object
    """
    with transaction.atomic():
        level_from_db = Level.objects.get(name=level)

        created_vacancy: Vacancy = Vacancy.objects.create(
            company=company,
            attachment=attachment_file,
            name=vacancy_name,
            level=level_from_db,
            experience=experience,
            min_salary=min_salary,
            max_salary=max_salary,
            description=description,
        )
        if tags:
            tags_list = re.split("[ \r\n]+", tags)
            result_tags_list = []
            for tag in tags_list:
                try:
                    tag_from_db = Tag.objects.get(name=tag)
                except Tag.DoesNotExist:
                    tag_from_db = Tag.objects.create(name=tag)
                result_tags_list.append(tag_from_db)
            created_vacancy.tags.set(result_tags_list)

        country_from_db = Country.objects.get(name=country)
        vacancy_cities_list = []
        cities_list = re.split("[ \r\n]+", cities)
        for city in cities_list:
            try:
                new_city = City.objects.get(name=city, country=country_from_db)
            except City.DoesNotExist:
                new_city = City.objects.create(name=city, country=country_from_db)
            vacancy_cities_list.append(new_city)
        employment_formats_list = []
        for employ_format in employment_formats:
            employment_format_from_db = EmploymentFormat.objects.get(name=employ_format)
            employment_formats_list.append(employment_format_from_db)
        work_formats_list = []
        for work_format in work_formats:
            work_format_from_db = WorkFormat.objects.get(name=work_format)
            work_formats_list.append(work_format_from_db)
        created_vacancy.city.set(vacancy_cities_list)
        created_vacancy.employment_format.set(employment_formats_list)
        created_vacancy.work_format.set(work_formats_list)
        return created_vacancy


def create_active_user_in_test_db(
    username: str, email: str, password: str = "test_password", role: str = "candidate"
) -> AbstractBaseUser:
    """Records the added User data in the database.

    :param username: name of created user. Must be unique.
    :type username: str
    :param password: password of created user.
    :type password: str
    :param email: email of created user. Must be unique. Default = "test@test.com".
    :type email: str
    :param role: role of created user. Can be "candidate" or "recruiter" . Default = "candidate".
    :type role: str
    """

    user_model: AbstractBaseUser = get_user_model()

    created_user: AbstractBaseUser = user_model.objects.create_user(
        username=username, password=password, email=email, is_active=True
    )
    group = Group.objects.get(name=role)
    created_user.groups.add(group)
    return created_user
