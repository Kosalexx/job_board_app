from core.business_logic.dto import AddVacancyDTO, SearchVacancyDTO
from core.business_logic.exceptions import (
    CompanyNotExistsError,
    CountryNotExistError,
    EmploymentFormatNotExistError,
    VacancyNotExistsError,
    WorkFormatNotExistError,
)
from core.business_logic.services import (
    create_vacancy,
    get_vacancies_by_company_id,
    get_vacancy_by_id,
    search_vacancies,
)
from core.models import City, Tag, Vacancy
from core.tests.mocks import QRApiAdapterMock
from core.tests.utils import create_test_company_in_db, create_test_vacancy_in_db, get_test_image, get_test_pdf
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase


class VacancyServicesTests(TestCase):
    """Contains all tests for services related to the vacancy endpoint."""

    def setUp(self) -> None:
        "Hook method for setting up the test fixture before exercising it."

        self.logo_for_test = get_test_image()
        self.attachment_for_test = get_test_pdf()
        self.company_1 = create_test_company_in_db(company_name='test_company_1', test_file=self.logo_for_test)
        self.company_2 = create_test_company_in_db(company_name='test_company_2', test_file=self.logo_for_test)
        self.company_3 = create_test_company_in_db(company_name='test_company_3', test_file=self.logo_for_test)
        self.vacancy_1 = create_test_vacancy_in_db(
            vacancy_name='Test_vacancy_1',
            company=self.company_1,
            attachment_file=self.attachment_for_test,
            min_salary=100,
            max_salary=1000,
            description='vac_1 description',
            employment_formats=['B2B'],
            work_formats=['Freelance', 'Part-time'],
            cities='Minsk',
            tags='python sql',
        )
        self.vacancy_2 = create_test_vacancy_in_db(
            vacancy_name='Test_vacancy_2', company=self.company_1, attachment_file=self.attachment_for_test
        )
        self.vacancy_3 = create_test_vacancy_in_db(
            vacancy_name='Test_vacancy_3', company=self.company_2, attachment_file=self.attachment_for_test
        )
        self.vacancy_4 = create_test_vacancy_in_db(
            vacancy_name='another_vacancy_1',
            company=self.company_3,
            attachment_file=self.attachment_for_test,
            level='Middle',
            experience='3+ years',
            min_salary=3000,
            max_salary=5000,
            description='Test description',
            tags='python sql',
            country="Armenia",
            cities='Erevan',
            employment_formats=['Mandate contract'],
            work_formats=['Office work', 'Part-time'],
        )
        result: None = super().setUp()
        return result

    def _get_add_vacancy_data(
        self,
        attachment: InMemoryUploadedFile,
        name: str = 'New_Test_vacancy',
        company_name: str = 'test_company_1',
        level: str = 'Junior',
        experience: str | None = '0 years',
        description: str | None = 'Test vacancy description',
        min_salary: int | None = 100,
        max_salary: int | None = 1000,
        employment_format: list = ['B2B', 'Employment contract'],  # noqa: B006
        work_format: list = ['Remote work', 'Hybrid'],  # noqa: B006
        country: str = 'Belarus',
        city: str = 'Minsk Brest',
        tags: str = 'tag1 tag2',
    ) -> AddVacancyDTO:
        """Creates AddCompanyProfileDTO with default values for further use in tests.

        :param attachment: File object that will be used as a vacancy attachment
        :type attachment: InMemoryUploadedFile
        :param name: created vacancy name. Default = 'New_Test_vacancy'
        :type name: str
        :param company_name: name of company that creates vacancy. Default = 'test_company_1'
        :type company_name: str
        :param level: required level of candidate. Default = 'Junior'
        :type level: str
        :param experience: required experience of candidate. Default = '0 years'
        :type experience: str | None
        :param description: vacancy description. Default = 'Test vacancy description'
        :type description: str | None
        :param min_salary: minimum salary bracket. Default = 100
        :type min_salary: int | None
        :param max_salary: maximum salary bracket. Default = 1000
        :type max_salary: int | None
        :param employment_format: possible employment formats. Default = ['B2B', 'Employment contract']
        :type employment_format: list
        :param work_format: possible work formats. Default = ['Remote work', 'Hybrid']
        :type work_format: list
        :param country: created vacancy country. Default = 'Belarus'
        :type country: str
        :param city: created vacancy possible cities (' '(space) separated). Default = 'Minsk Brest'
        :type city: str
        :param tags: created vacancy related tags (' '(space) separated). Default = 'tag1 tag2'
        :type tags: str

        :rtype: AddVacancyDTO
        :return: data transfer object with data about created vacancy
        """
        return AddVacancyDTO(
            name=name,
            company_name=company_name,
            attachment=attachment,
            level=level,
            experience=experience,
            description=description,
            min_salary=min_salary,
            max_salary=max_salary,
            employment_format=employment_format,
            work_format=work_format,
            country=country,
            city=city,
            tags=tags,
        )

    def _get_search_vacancy_data(
        self,
        name: str = '',
        company_name: str = '',
        level: str = '',
        experience: str = '',
        description: str | None = '',
        min_salary: int | None = None,
        max_salary: int | None = None,
        employment_format: list = [],  # noqa: B006
        work_format: list = [],  # noqa: B006
        country: str = '',
        city: str = '',
        tag: str = '',
    ) -> SearchVacancyDTO:
        """Creates SearchVacancyDTO with default empty values for further use in tests.

        :param name: searched vacancy name. Default = ''
        :type name: str
        :param company_name: name of company that creates vacancy. Default = ''
        :type company_name: str
        :param level: required level of candidate. Default = ''
        :type level: str
        :param experience: required experience of candidate. Default = ''
        :type experience: str
        :param description: vacancy description. Default = ''
        :type description: str
        :param min_salary: minimum salary bracket. Default = None
        :type min_salary: int | None
        :param max_salary: maximum salary bracket. Default = None
        :type max_salary: int | None
        :param employment_format: searched vacancy employment formats. Default = []
        :type employment_format: list
        :param work_format: searched vacancy possible work formats. Default = []
        :type work_format: list
        :param country: searched vacancy country. Default = ''
        :type country: str
        :param city: searched vacancy possible city. Default = ''
        :type city: str
        :param tags: searched vacancy related tag. Default = ''
        :type tags: str

        :rtype: SearchVacancyDTO
        :return: data transfer object with data about searched vacancy
        """
        result = SearchVacancyDTO(
            name=name,
            company_name=company_name,
            level=level,
            experience=experience,
            description=description,
            min_salary=min_salary,
            max_salary=max_salary,
            employment_format=employment_format,
            work_format=work_format,
            country=country,
            city=city,
            tag=tag,
        )
        return result

    def test_create_vacancy_successfully(self) -> None:
        """Checks the correctness of vacancy creation in the database."""

        vacancy_data = self._get_add_vacancy_data(attachment=self.attachment_for_test, name='Python Developer')
        count_before_request = Vacancy.objects.all().count()
        qr_adapter = QRApiAdapterMock()
        created_vacancy_id = create_vacancy(data=vacancy_data, qr_adapter=qr_adapter)
        self.assertIsInstance(created_vacancy_id, int)
        count_after_request = Vacancy.objects.all().count()
        self.assertEqual(count_before_request + 1, count_after_request)
        vacancy_from_db: Vacancy = (
            Vacancy.objects.select_related("level", "company").prefetch_related("tags").get(name=vacancy_data.name)
        )
        self.assertEqual(vacancy_from_db.name, vacancy_data.name)
        self.assertEqual(vacancy_from_db.level.name, vacancy_data.level)
        self.assertEqual(vacancy_from_db.experience, vacancy_data.experience)
        self.assertEqual(vacancy_from_db.company.name, vacancy_data.company_name)
        self.assertEqual(vacancy_from_db.min_salary, vacancy_data.min_salary)
        self.assertEqual(vacancy_from_db.max_salary, vacancy_data.max_salary)
        self.assertEqual(vacancy_from_db.description, vacancy_data.description)
        expected_tags = vacancy_data.tags
        tags_from_db = vacancy_from_db.tags.all()
        for tag in tags_from_db:
            self.assertIn(tag.name, expected_tags)

        expected_employment_formats = vacancy_data.employment_format
        employment_formats_from_db = vacancy_from_db.employment_format.all()
        for employ_format in employment_formats_from_db:
            self.assertIn(employ_format.name, expected_employment_formats)

        expected_work_formats = vacancy_data.work_format
        work_formats_from_db = vacancy_from_db.work_format.all()
        for work_format in work_formats_from_db:
            self.assertIn(work_format.name, expected_work_formats)

        expected_cities = vacancy_data.city.split()
        cities_from_db = vacancy_from_db.city.all()
        for city in cities_from_db:
            self.assertIn(city.name, expected_cities)
            self.assertEqual(city.country.name, vacancy_data.country)

    def test_create_vacancy_with_invalid_company(self) -> None:
        """Checks if an exception is raised if specified invalid company name."""

        vacancy_data = self._get_add_vacancy_data(
            attachment=self.attachment_for_test, company_name='Invalid Company name'
        )
        count_vacancies_before_request = Vacancy.objects.all().count()
        count_tags_before_request = Tag.objects.all().count()
        count_cities_before_request = City.objects.all().count()
        with self.assertRaises(CompanyNotExistsError):
            qr_adapter = QRApiAdapterMock()
            create_vacancy(vacancy_data, qr_adapter=qr_adapter)
        count_vacancies_after_request = Vacancy.objects.all().count()
        count_tags_after_request = Tag.objects.all().count()
        count_cities_after_request = City.objects.all().count()
        self.assertEqual(count_vacancies_before_request, count_vacancies_after_request)
        self.assertEqual(count_tags_before_request, count_tags_after_request)
        self.assertEqual(count_cities_before_request, count_cities_after_request)

    def test_create_vacancy_with_invalid_country(self) -> None:
        """Checks if an exception is raised if specified invalid country name."""

        vacancy_data = self._get_add_vacancy_data(attachment=self.attachment_for_test, country='Invalid Country name')
        count_vacancies_before_request = Vacancy.objects.all().count()
        count_tags_before_request = Tag.objects.all().count()
        count_cities_before_request = City.objects.all().count()
        with self.assertRaises(CountryNotExistError):
            qr_adapter = QRApiAdapterMock()
            create_vacancy(vacancy_data, qr_adapter=qr_adapter)
        count_vacancies_after_request = Vacancy.objects.all().count()
        count_tags_after_request = Tag.objects.all().count()
        count_cities_after_request = City.objects.all().count()
        self.assertEqual(count_vacancies_before_request, count_vacancies_after_request)
        self.assertEqual(count_tags_before_request, count_tags_after_request)
        self.assertEqual(count_cities_before_request, count_cities_after_request)

    def test_create_vacancy_with_invalid_employment_formats(self) -> None:
        """Checks if an exception is raised if specified invalid employment format."""

        vacancy_data = self._get_add_vacancy_data(
            attachment=self.attachment_for_test, employment_format=['Invalid', 'Formats']
        )
        count_vacancies_before_request = Vacancy.objects.all().count()
        count_tags_before_request = Tag.objects.all().count()
        count_cities_before_request = City.objects.all().count()
        with self.assertRaises(EmploymentFormatNotExistError):
            qr_adapter = QRApiAdapterMock()
            create_vacancy(vacancy_data, qr_adapter=qr_adapter)
        count_vacancies_after_request = Vacancy.objects.all().count()
        count_tags_after_request = Tag.objects.all().count()
        count_cities_after_request = City.objects.all().count()
        self.assertEqual(count_vacancies_before_request, count_vacancies_after_request)
        self.assertEqual(count_tags_before_request, count_tags_after_request)
        self.assertEqual(count_cities_before_request, count_cities_after_request)

    def test_create_vacancy_with_invalid_work_formats(self) -> None:
        """Checks if an exception is raised if specified invalid work format."""

        vacancy_data = self._get_add_vacancy_data(
            attachment=self.attachment_for_test, work_format=['Invalid', 'Formats']
        )
        count_vacancies_before_request = Vacancy.objects.all().count()
        count_tags_before_request = Tag.objects.all().count()
        count_cities_before_request = City.objects.all().count()
        with self.assertRaises(WorkFormatNotExistError):
            qr_adapter = QRApiAdapterMock()
            create_vacancy(vacancy_data, qr_adapter=qr_adapter)
        count_vacancies_after_request = Vacancy.objects.all().count()
        count_tags_after_request = Tag.objects.all().count()
        count_cities_after_request = City.objects.all().count()
        self.assertEqual(count_vacancies_before_request, count_vacancies_after_request)
        self.assertEqual(count_tags_before_request, count_tags_after_request)
        self.assertEqual(count_cities_before_request, count_cities_after_request)

    def test_get_vacancy_by_invalid_id(self) -> None:
        """Checks if an exception is raises if company with specified company_id doesn't exist in the database."""

        vacancy_id = 9999999999999999
        with self.assertRaises(VacancyNotExistsError):
            get_vacancy_by_id(vacancy_id=vacancy_id)
        with self.assertRaises(Vacancy.DoesNotExist):
            Vacancy.objects.get(pk=vacancy_id)

    def test_get_vacancy_by_id_successfully(self) -> None:
        """Checks correctness of getting vacancy by entered vacancy_id."""

        vacancy_id = self.vacancy_1.pk
        vacancy_from_func = get_vacancy_by_id(vacancy_id=vacancy_id)
        self.assertEqual(self.vacancy_1.pk, vacancy_from_func.vacancy.pk)
        self.assertEqual(self.vacancy_1.name, vacancy_from_func.vacancy.name)
        self.assertEqual(self.vacancy_1.level, vacancy_from_func.vacancy.level)
        self.assertEqual(self.vacancy_1.experience, vacancy_from_func.vacancy.experience)
        self.assertEqual(self.vacancy_1.min_salary, vacancy_from_func.vacancy.min_salary)
        self.assertEqual(self.vacancy_1.max_salary, vacancy_from_func.vacancy.max_salary)
        self.assertEqual(self.vacancy_1.company, vacancy_from_func.vacancy.company)
        self.assertEqual(self.vacancy_1.tags, vacancy_from_func.vacancy.tags)
        self.assertEqual(list(self.vacancy_1.tags.all()), vacancy_from_func.tags)
        self.assertEqual(self.vacancy_1.employment_format, vacancy_from_func.vacancy.employment_format)
        self.assertEqual(list(self.vacancy_1.employment_format.all()), vacancy_from_func.employment_format)
        self.assertEqual(self.vacancy_1.description, vacancy_from_func.vacancy.description)
        self.assertEqual(self.vacancy_1.work_format, vacancy_from_func.vacancy.work_format)
        self.assertEqual(list(self.vacancy_1.work_format.all()), vacancy_from_func.work_format)
        self.assertEqual(self.vacancy_1.city, vacancy_from_func.vacancy.city)
        self.assertEqual(list(self.vacancy_1.city.all()), vacancy_from_func.city)

        vacancy_from_db = Vacancy.objects.get(pk=vacancy_id)

        self.assertEqual(vacancy_from_db.pk, vacancy_from_func.vacancy.pk)
        self.assertEqual(vacancy_from_db.name, vacancy_from_func.vacancy.name)
        self.assertEqual(vacancy_from_db.level, vacancy_from_func.vacancy.level)
        self.assertEqual(vacancy_from_db.experience, vacancy_from_func.vacancy.experience)
        self.assertEqual(vacancy_from_db.min_salary, vacancy_from_func.vacancy.min_salary)
        self.assertEqual(vacancy_from_db.max_salary, vacancy_from_func.vacancy.max_salary)
        self.assertEqual(vacancy_from_db.company, vacancy_from_func.vacancy.company)
        self.assertEqual(vacancy_from_db.tags, vacancy_from_func.vacancy.tags)
        self.assertEqual(list(vacancy_from_db.tags.all()), vacancy_from_func.tags)
        self.assertEqual(vacancy_from_db.employment_format, vacancy_from_func.vacancy.employment_format)
        self.assertEqual(list(vacancy_from_db.employment_format.all()), vacancy_from_func.employment_format)
        self.assertEqual(vacancy_from_db.description, vacancy_from_func.vacancy.description)
        self.assertEqual(vacancy_from_db.work_format, vacancy_from_func.vacancy.work_format)
        self.assertEqual(list(vacancy_from_db.work_format.all()), vacancy_from_func.work_format)
        self.assertEqual(vacancy_from_db.city, vacancy_from_func.vacancy.city)
        self.assertEqual(list(vacancy_from_db.city.all()), vacancy_from_func.city)

    def test_get_vacancies_by_company_id_successfully(self) -> None:
        """Checks correctness of getting vacancies list by entered company_id."""

        company_1_id = self.company_1.pk
        result_company_1_vacancies_list = get_vacancies_by_company_id(company_id=company_1_id)
        expected_vacancies = [Vacancy.objects.get(name='Test_vacancy_1'), Vacancy.objects.get(name='Test_vacancy_2')]
        for vacancy in result_company_1_vacancies_list:
            self.assertIn(vacancy, expected_vacancies)
        company_2_id = self.company_2.pk
        result_company_2_vacancies_list = get_vacancies_by_company_id(company_id=company_2_id)
        expected_vacancies = [
            Vacancy.objects.get(name='Test_vacancy_3'),
        ]
        for vacancy in result_company_2_vacancies_list:
            self.assertIn(vacancy, expected_vacancies)
        # if an invalid company name is passed, the function will return an empty list []
        invalid_company_id = 999999999999999
        result_vacancies_list_by_invalid_company = get_vacancies_by_company_id(company_id=invalid_company_id)
        self.assertEqual(result_vacancies_list_by_invalid_company, [])

    def test_search_vacancies_all_filters(self) -> None:
        """Checks correctness of searching vacancies if all filters specified."""

        all_filters_dto = self._get_search_vacancy_data(
            name='another_vacancy_1',
            company_name='test_company_3',
            level='Middle',
            experience='3+ years',
            min_salary=3000,
            max_salary=5000,
            description='Test description',
            employment_format=['Mandate contract'],
            work_format=['Office work'],
            country='Armenia',
            city='Erevan',
            tag='python',
        )
        result_queryset = search_vacancies(all_filters_dto)
        self.assertEqual(len(result_queryset), 1)
        self.assertIn(self.vacancy_4, result_queryset)

    def test_search_vacancies_empty_filters(self) -> None:
        """Checks correctness of searching vacancies if empty filters."""

        empty_filters_dto = self._get_search_vacancy_data()
        result_queryset = search_vacancies(empty_filters_dto)
        self.assertEqual(len(result_queryset), 4)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_2, result_queryset)
        self.assertIn(self.vacancy_3, result_queryset)
        self.assertIn(self.vacancy_4, result_queryset)

    def test_search_vacancies_by_name_filter(self) -> None:
        """Checks correctness of searching vacancies if name filter specified."""

        vacancies_data = self._get_search_vacancy_data(name='_1')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 2)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_4, result_queryset)
        vacancies_data_2 = self._get_search_vacancy_data(name='vacancy')
        result_queryset_2 = search_vacancies(vacancies_data_2)
        self.assertEqual(len(result_queryset_2), 4)
        self.assertIn(self.vacancy_1, result_queryset_2)
        self.assertIn(self.vacancy_2, result_queryset_2)
        self.assertIn(self.vacancy_3, result_queryset_2)
        self.assertIn(self.vacancy_4, result_queryset_2)
        vacancies_data_3 = self._get_search_vacancy_data(name='test')
        result_queryset_3 = search_vacancies(vacancies_data_3)
        self.assertEqual(len(result_queryset_3), 3)
        self.assertIn(self.vacancy_1, result_queryset_3)
        self.assertIn(self.vacancy_2, result_queryset_3)
        self.assertIn(self.vacancy_3, result_queryset_3)
        vacancies_data = self._get_search_vacancy_data(name='Non-existent vacancy')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 0)

    def test_search_vacancies_by_company_filter(self) -> None:
        """Checks correctness of searching vacancies if company_name filter specified."""

        vacancies_data = self._get_search_vacancy_data(company_name='test_company_1')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 2)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_2, result_queryset)
        vacancies_data_2 = self._get_search_vacancy_data(company_name='test_company_2')
        result_queryset = search_vacancies(vacancies_data_2)
        self.assertEqual(len(result_queryset), 1)
        self.assertIn(self.vacancy_3, result_queryset)
        vacancies_data_3 = self._get_search_vacancy_data(company_name='test_company_')
        result_queryset = search_vacancies(vacancies_data_3)
        self.assertEqual(len(result_queryset), 4)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_2, result_queryset)
        self.assertIn(self.vacancy_3, result_queryset)
        self.assertIn(self.vacancy_4, result_queryset)

    def test_search_vacancies_by_name_and_company_filter(self) -> None:
        """Checks correctness of searching vacancies if name and company_name filter specified."""

        vacancies_data = self._get_search_vacancy_data(name='Test', company_name='test_company_1')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 2)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_2, result_queryset)
        vacancies_data = self._get_search_vacancy_data(name='Non-existent vacancy', company_name='test_company_1')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 0)
        vacancies_data = self._get_search_vacancy_data(name='Test_vacancy_3', company_name='test_company_1')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 0)

    def test_search_vacancies_by_level_filter(self) -> None:
        """Checks correctness of searching vacancies if level filter specified."""

        vacancies_data = self._get_search_vacancy_data(level='Junior')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 3)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_2, result_queryset)
        self.assertIn(self.vacancy_3, result_queryset)
        vacancies_data_2 = self._get_search_vacancy_data(level='Middle')
        result_queryset = search_vacancies(vacancies_data_2)
        self.assertEqual(len(result_queryset), 1)
        self.assertIn(self.vacancy_4, result_queryset)
        vacancies_data_3 = self._get_search_vacancy_data(level='Senior')
        result_queryset = search_vacancies(vacancies_data_3)
        self.assertEqual(len(result_queryset), 0)

    def test_search_vacancies_by_name_and_level_filter(self) -> None:
        """Checks correctness of searching vacancies if level and name filters specified."""

        vacancies_data = self._get_search_vacancy_data(name='vacancy', level='Junior')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 3)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_2, result_queryset)
        self.assertIn(self.vacancy_3, result_queryset)
        vacancies_data = self._get_search_vacancy_data(name='vacancy_1', level='Junior')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 1)
        self.assertIn(self.vacancy_1, result_queryset)
        vacancies_data = self._get_search_vacancy_data(name='vacancy_2', level='Junior')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 1)
        self.assertIn(self.vacancy_2, result_queryset)
        vacancies_data = self._get_search_vacancy_data(name='vacancy_3', level='Junior')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 1)
        self.assertIn(self.vacancy_3, result_queryset)
        vacancies_data = self._get_search_vacancy_data(name='Nonexistent vacancy', level='Junior')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 0)
        vacancies_data = self._get_search_vacancy_data(name='vacancy_1', level='Middle')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 1)
        self.assertIn(self.vacancy_4, result_queryset)
        vacancies_data = self._get_search_vacancy_data(name='vacancy_2', level='Middle')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 0)
        vacancies_data_3 = self._get_search_vacancy_data(name='vacancy', level='Senior')
        result_queryset = search_vacancies(vacancies_data_3)
        self.assertEqual(len(result_queryset), 0)

    def test_search_vacancies_by_experience_filter(self) -> None:
        """Checks correctness of searching vacancies if experience filters specified."""

        vacancies_data = self._get_search_vacancy_data(experience='0')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 3)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_2, result_queryset)
        self.assertIn(self.vacancy_3, result_queryset)
        vacancies_data = self._get_search_vacancy_data(experience='3+')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 1)
        self.assertIn(self.vacancy_4, result_queryset)
        vacancies_data = self._get_search_vacancy_data(experience='invalid value')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 0)

    def test_search_vacancies_by_description_filter(self) -> None:
        """Checks correctness of searching vacancies if description filters specified."""

        vacancies_data = self._get_search_vacancy_data(description='description')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 2)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_4, result_queryset)
        for vac in result_queryset:
            self.assertIn('description', vac.description)

        vacancies_data = self._get_search_vacancy_data(description='vac_1')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 1)
        self.assertIn(self.vacancy_1, result_queryset)
        for vac in result_queryset:
            self.assertIn('vac_1', vac.description)
        vacancies_data = self._get_search_vacancy_data(description='Test')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 1)
        self.assertIn(self.vacancy_4, result_queryset)
        for vac in result_queryset:
            self.assertIn('Test', vac.description)
        vacancies_data = self._get_search_vacancy_data(description='Nonexistent description')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 0)

    def test_search_vacancies_by_min_salary_filter(self) -> None:
        """Checks correctness of searching vacancies if min_salary filters specified."""

        vacancies_data = self._get_search_vacancy_data(min_salary=100)
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 2)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_4, result_queryset)
        vacancies_data = self._get_search_vacancy_data(min_salary=1000)
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 1)
        self.assertIn(self.vacancy_4, result_queryset)
        vacancies_data = self._get_search_vacancy_data(min_salary=500)
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 1)
        self.assertIn(self.vacancy_4, result_queryset)
        vacancies_data = self._get_search_vacancy_data(min_salary=999999999999)
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 0)

    def test_search_vacancies_by_max_salary_filter(self) -> None:
        """Checks correctness of searching vacancies if max_salary filters specified."""

        vacancies_data = self._get_search_vacancy_data(max_salary=5000)
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 2)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_4, result_queryset)
        vacancies_data = self._get_search_vacancy_data(max_salary=1000)
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 1)
        self.assertIn(self.vacancy_1, result_queryset)
        vacancies_data = self._get_search_vacancy_data(max_salary=500)
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 0)
        vacancies_data = self._get_search_vacancy_data(max_salary=999999999999)
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 2)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_4, result_queryset)

    def test_search_vacancies_by_employment_format_filter(self) -> None:
        """Checks correctness of searching vacancies if employment_format filters specified."""

        vacancies_data = self._get_search_vacancy_data(
            employment_format=['B2B', 'Employment contract', 'Mandate contract']
        )
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 4)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_2, result_queryset)
        self.assertIn(self.vacancy_3, result_queryset)
        self.assertIn(self.vacancy_4, result_queryset)
        vacancies_data = self._get_search_vacancy_data(
            employment_format=[
                'B2B',
            ]
        )
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 3)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_2, result_queryset)
        self.assertIn(self.vacancy_3, result_queryset)
        vacancies_data = self._get_search_vacancy_data(
            employment_format=[
                'Employment contract',
            ]
        )
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 2)
        self.assertIn(self.vacancy_2, result_queryset)
        self.assertIn(self.vacancy_3, result_queryset)
        vacancies_data = self._get_search_vacancy_data(
            employment_format=[
                'Mandate contract',
            ]
        )
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 1)
        self.assertIn(self.vacancy_4, result_queryset)
        vacancies_data = self._get_search_vacancy_data(employment_format=['Employment contract', 'Mandate contract'])
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 3)
        self.assertIn(self.vacancy_2, result_queryset)
        self.assertIn(self.vacancy_3, result_queryset)
        self.assertIn(self.vacancy_4, result_queryset)
        vacancies_data = self._get_search_vacancy_data(employment_format=['B2B', 'Mandate contract'])
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 4)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_2, result_queryset)
        self.assertIn(self.vacancy_3, result_queryset)
        self.assertIn(self.vacancy_4, result_queryset)

    def test_search_vacancies_by_work_format_filter(self) -> None:
        """Checks correctness of searching vacancies if work_format filters specified."""

        vacancies_data = self._get_search_vacancy_data(
            work_format=['Remote work', 'Hybrid', 'Freelance', 'Part-time', 'Full-time', 'Office work']
        )
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 4)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_2, result_queryset)
        self.assertIn(self.vacancy_3, result_queryset)
        self.assertIn(self.vacancy_4, result_queryset)
        vacancies_data = self._get_search_vacancy_data(work_format=['Remote work', 'Hybrid'])
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 2)
        self.assertIn(self.vacancy_2, result_queryset)
        self.assertIn(self.vacancy_3, result_queryset)
        vacancies_data = self._get_search_vacancy_data(work_format=['Remote work'])
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 2)
        self.assertIn(self.vacancy_2, result_queryset)
        self.assertIn(self.vacancy_3, result_queryset)
        vacancies_data = self._get_search_vacancy_data(work_format=['Hybrid'])
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 2)
        self.assertIn(self.vacancy_2, result_queryset)
        self.assertIn(self.vacancy_3, result_queryset)
        vacancies_data = self._get_search_vacancy_data(work_format=['Part-time'])
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 2)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_4, result_queryset)
        vacancies_data = self._get_search_vacancy_data(work_format=['Freelance'])
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 1)
        self.assertIn(self.vacancy_1, result_queryset)
        vacancies_data = self._get_search_vacancy_data(work_format=['Office work'])
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 1)
        self.assertIn(self.vacancy_4, result_queryset)
        vacancies_data = self._get_search_vacancy_data(work_format=['Office work', 'Freelance'])
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 2)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_4, result_queryset)
        vacancies_data = self._get_search_vacancy_data(work_format=['Full-time'])
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 0)

    def test_search_vacancies_by_country_filter(self) -> None:
        """Checks correctness of searching vacancies if country filters specified."""

        vacancies_data = self._get_search_vacancy_data(country='Belarus')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 3)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_2, result_queryset)
        self.assertIn(self.vacancy_3, result_queryset)
        vacancies_data = self._get_search_vacancy_data(country='Armenia')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 1)
        self.assertIn(self.vacancy_4, result_queryset)
        vacancies_data = self._get_search_vacancy_data(country='Angola')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 0)

    def test_search_vacancies_by_city_filter(self) -> None:
        """Checks correctness of searching vacancies if city filters specified."""

        vacancies_data = self._get_search_vacancy_data(city='Minsk')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 3)
        self.assertIn(self.vacancy_1, result_queryset)
        self.assertIn(self.vacancy_2, result_queryset)
        self.assertIn(self.vacancy_3, result_queryset)

        vacancies_data = self._get_search_vacancy_data(city='Brest')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 2)
        self.assertIn(self.vacancy_2, result_queryset)
        self.assertIn(self.vacancy_3, result_queryset)
        vacancies_data = self._get_search_vacancy_data(city='Erevan')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 1)
        self.assertIn(self.vacancy_4, result_queryset)
        vacancies_data = self._get_search_vacancy_data(city='Invalid city name')
        result_queryset = search_vacancies(vacancies_data)
        self.assertEqual(len(result_queryset), 0)
