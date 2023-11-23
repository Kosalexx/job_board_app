import pytest
from core.business_logic.dto import AddAddressDTO, AddCompanyDTO, AddCompanyProfileDTO
from core.business_logic.exceptions import (
    CompanyAlreadyExistsError,
    CompanyNotExistsError,
    CompanyProfileNotExistsError,
    CountryNotExistError,
)
from core.business_logic.services import create_company, get_companies, get_company_by_id, get_company_profile_by_id
from core.models import Address, BusinessArea, City, Company, CompanyProfile
from django.core.files.uploadedfile import InMemoryUploadedFile


def get_company_data(name: str = 'TEST', staff: int = 100, business_area: str = 'test1 test2') -> AddCompanyDTO:
    """Creates CompanyDTO for further use in tests.

    :param name: name of created company. Default = 'TEST'
    :type name: str
    :param staff: created company employees number. Default = 100
    :type staff: int
    :param business_area: names of business areas (' '(space) separated). Default = 'test1 test2'
    :type business_area: str

    :rtype: AddCompanyDTO
    :return: data transfer object with data about created company
    """
    company_data = AddCompanyDTO(name=name, staff=staff, business_area=business_area)
    return company_data


def get_company_profile_data(
    logo: InMemoryUploadedFile,
    email: str = 'test@test.com',
    founding_year: int = 2000,
    description: str = 'Test description',
    phone: str = '+1111111',
    website_link: str = 'test.com',
    linkedin_link: None | str = None,
    github_link: None | str = None,
    twitter_link: None | str = None,
) -> AddCompanyProfileDTO:
    """Creates AddCompanyProfileDTO for further use in tests.

    :param logo: File object that will be used as a company logo
    :type logo: InMemoryUploadedFile
    :param email: created company email. Default = 'test@test.com'
    :type email: str
    :param founding_year: names of business areas (' '(space) separated). Default = 'test1 test2'
    :type founding_year: int
    :param description: company description. Default = 'Test description'
    :type description: str
    :param phone: company phone. Default = '+1111111'
    :type phone: str
    :param website_link: company website link. Default = 'test.com'
    :type website_link: str
    :param linkedin_link: company profile on LinkedIn. Default = None
    :type linkedin_link: str | None
    :param github_link: company profile on GitHub. Default = None
    :type github_link: str | None
    :param twitter_link: company profile on Twitter(X). Default = None
    :type twitter_link: str | None

    :rtype: AddCompanyProfileDTO
    :return: data transfer object with data about created company profile
    """
    profile_data = AddCompanyProfileDTO(
        logo=logo,
        email=email,
        founding_year=founding_year,
        description=description,
        phone=phone,
        website_link=website_link,
        linkedin_link=linkedin_link,
        github_link=github_link,
        twitter_link=twitter_link,
    )
    return profile_data


def get_address_data(
    country: str = 'Belarus',
    city: str = 'Minsk',
    street_name: str = '1st',
    home_number: int = 1,
    office_number: int | None = None,
) -> AddAddressDTO:
    """Creates AddAddressDTO for further use in tests.

    :param country: name of country. A Country with the specified name must exist in database. Default = 'Belarus'
    :type country: str
    :param city: name of city. Default = 'Minsk'
    :type city: str
    :param street_name: name of street. Default = '1st'
    :type street_name: str
    :param home_number: number of home. Default = 1
    :type home_number: int
    :param office_number: number of office. Default = None
    :type office_number: str | None

    :rtype: AddAddressDTO
    :return: data transfer object with data about created company address
    """
    address_data = AddAddressDTO(
        country=country, city=city, street_name=street_name, home_number=home_number, office_number=office_number
    )
    return address_data


@pytest.mark.django_db
def test_create_company_successfully(png_for_test: InMemoryUploadedFile) -> None:
    """Checks the correctness of company creation in the database."""

    company_data = get_company_data(name='EPAM', staff=1000, business_area='web finance')
    profile_data = get_company_profile_data(logo=png_for_test)
    address_data = get_address_data()
    count_companies_before_request = Company.objects.all().count()
    count_company_profiles_before_request = CompanyProfile.objects.all().count()
    company_id = create_company(company_data=company_data, profile_data=profile_data, address_data=address_data)
    count_companies_after_request = Company.objects.all().count()
    count_company_profiles_after_request = CompanyProfile.objects.all().count()
    assert isinstance(company_id, int)
    assert count_companies_before_request + 1 == count_companies_after_request
    assert count_company_profiles_before_request + 1 == count_company_profiles_after_request

    company_from_db = Company.objects.get(pk=company_id)
    assert company_from_db.name == company_data.name
    assert company_from_db.staff == company_data.staff
    assert company_from_db.company_profile.email == profile_data.email
    assert company_from_db.company_profile.founding_year == profile_data.founding_year
    assert company_from_db.company_profile.description == profile_data.description
    assert company_from_db.company_profile.phone == profile_data.phone
    assert company_from_db.company_profile.website_link == profile_data.website_link
    assert company_from_db.company_profile.linkedin_link == profile_data.linkedin_link
    assert company_from_db.company_profile.github_link == profile_data.github_link
    assert company_from_db.company_profile.twitter_link == profile_data.twitter_link
    assert company_from_db.company_profile.address.office_number == address_data.office_number
    assert company_from_db.company_profile.address.home_number == address_data.home_number
    assert company_from_db.company_profile.address.street_name == address_data.street_name
    assert company_from_db.company_profile.address.city.country.name == address_data.country
    assert company_from_db.company_profile.address.city.name == address_data.city

    expected_business_areas = ('web', 'finance')
    business_areas_from_db = company_from_db.business_area.all()
    assert len(expected_business_areas) == len(business_areas_from_db)
    for area in business_areas_from_db:
        assert area.name in expected_business_areas


@pytest.mark.django_db
def test_create_company_by_duplicate_name(png_for_test: InMemoryUploadedFile) -> None:
    """Checks if an exception is raised if a company with the specified name already exists in the database."""

    company_data_1 = get_company_data(name='test_company_1', business_area='random_area1 random_area2')
    company_profile_data_1 = get_company_profile_data(logo=png_for_test)
    address_data_1 = get_address_data(country="Angola", city="Random City")
    count_companies_before_request = Company.objects.all().count()
    count_company_profiles_before_request = CompanyProfile.objects.all().count()
    count_addresses_before_request = Address.objects.all().count()
    count_cities_before_request = City.objects.all().count()
    count_business_areas_before_request = BusinessArea.objects.all().count()
    with pytest.raises(CompanyAlreadyExistsError):
        create_company(company_data_1, company_profile_data_1, address_data_1)
    count_companies_after_request = Company.objects.all().count()
    count_company_profiles_after_request = CompanyProfile.objects.all().count()
    count_addresses_after_request = Address.objects.all().count()
    count_cities_after_request = City.objects.all().count()
    count_business_areas_after_request = BusinessArea.objects.all().count()
    assert count_companies_before_request == count_companies_after_request
    assert count_company_profiles_before_request == count_company_profiles_after_request
    assert count_addresses_before_request == count_addresses_after_request
    assert count_cities_before_request == count_cities_after_request
    assert count_business_areas_before_request == count_business_areas_after_request


@pytest.mark.django_db
def test_create_company_with_nonexistent_country(png_for_test: InMemoryUploadedFile) -> None:
    """Checks if an exception is raised if specified non-existent country name."""

    company_data_1 = get_company_data()
    company_profile_data_1 = get_company_profile_data(logo=png_for_test)
    address_data_1 = get_address_data(country="Wrong Country Name", city="Random City")
    count_companies_before_request = Company.objects.all().count()
    count_company_profiles_before_request = CompanyProfile.objects.all().count()
    count_addresses_before_request = Address.objects.all().count()
    count_cities_before_request = City.objects.all().count()
    count_business_areas_before_request = BusinessArea.objects.all().count()
    with pytest.raises(CountryNotExistError):
        create_company(company_data_1, company_profile_data_1, address_data_1)
    count_companies_after_request = Company.objects.all().count()
    count_company_profiles_after_request = CompanyProfile.objects.all().count()
    count_addresses_after_request = Address.objects.all().count()
    count_cities_after_request = City.objects.all().count()
    count_business_areas_after_request = BusinessArea.objects.all().count()
    assert count_companies_before_request == count_companies_after_request
    assert count_company_profiles_before_request == count_company_profiles_after_request
    assert count_addresses_before_request == count_addresses_after_request
    assert count_cities_before_request == count_cities_after_request
    assert count_business_areas_before_request == count_business_areas_after_request


@pytest.mark.django_db
def test_get_all_companies_successfully() -> None:
    """Checks correctness of getting the list of all companies from the database."""

    result_companies_list = get_companies()
    company_names = [row.name for row in result_companies_list]

    assert len(result_companies_list) == 3
    assert 'test_company_1' in company_names
    assert 'test_company_2' in company_names
    assert 'test_company_3' in company_names


@pytest.mark.django_db
def test_get_company_by_id_successfully() -> None:
    """Checks correctness of getting company by entered company_id from the database."""

    company = Company.objects.get(name='test_company_1')
    company_id = company.pk
    result = get_company_by_id(company_id=company_id)

    assert result.pk == company_id
    assert result.name == "test_company_1"


@pytest.mark.django_db
def test_get_company_by_invalid_id() -> None:
    """Checks if an exception is raises if company with specified company_id doesn't exist in the database."""

    company_id = 9999999999999
    with pytest.raises(CompanyNotExistsError):
        get_company_by_id(company_id=company_id)

    with pytest.raises(Company.DoesNotExist):
        Company.objects.get(pk=company_id)


@pytest.mark.django_db
def test_get_company_profile_by_id_successfully() -> None:
    """Checks correctness of getting company profile by entered company_id from the database."""

    company_from_db = Company.objects.get(name='test_company_1')
    company_id = company_from_db.pk
    company = get_company_by_id(company_id=company_id)

    profile_from_db = CompanyProfile.objects.get(pk=company_id)
    company_profile = get_company_profile_by_id(company_id=company_id)
    # checks if profile from function equal as profile from db
    assert profile_from_db.logo == company_profile.logo
    assert profile_from_db.email == company_profile.email
    assert profile_from_db.founding_year == company_profile.founding_year
    assert profile_from_db.description == company_profile.description
    assert profile_from_db.phone == company_profile.phone
    assert profile_from_db.website_link == company_profile.website_link
    assert profile_from_db.linkedin_link == company_profile.linkedin_link
    assert profile_from_db.github_link == company_profile.github_link
    assert profile_from_db.twitter_link == company_profile.twitter_link
    assert profile_from_db.address == company_profile.address
    assert profile_from_db.company == company_profile.company
    # checks correctness of One to One relation between Company and CompanyProfile entities
    assert company.company_profile.logo == company_profile.logo
    assert company.company_profile.email == company_profile.email
    assert company.company_profile.founding_year == company_profile.founding_year
    assert company.company_profile.description == company_profile.description
    assert company.company_profile.phone == company_profile.phone
    assert company.company_profile.website_link == company_profile.website_link
    assert company.company_profile.linkedin_link == company_profile.linkedin_link
    assert company.company_profile.github_link == company_profile.github_link
    assert company.company_profile.twitter_link == company_profile.twitter_link
    assert company.company_profile.address == company_profile.address
    assert company.company_profile.company == company_profile.company


@pytest.mark.django_db
def test_get_company_profile_by_id_failed() -> None:
    """Checks if an exception is raises if company with specified company_id doesn't exist in the database."""

    company_id = 99999999999999999
    with pytest.raises(CompanyProfileNotExistsError):
        get_company_profile_by_id(company_id=company_id)

    with pytest.raises(CompanyProfile.DoesNotExist):
        CompanyProfile.objects.get(pk=company_id)


@pytest.mark.django_db
def test_get_companies_order_by_vacancy_count() -> None:
    """Checks if the data order is correct when retrieving the list of companies from the database."""

    result_companies_list = get_companies()
    for ind in range(1, len(result_companies_list)):
        assert result_companies_list[ind].vacancy__count <= result_companies_list[ind - 2].vacancy__count
