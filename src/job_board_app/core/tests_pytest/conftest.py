import io
from dataclasses import dataclass

import pytest
from core.models import Company, Vacancy
from core.tests_pytest.mocks import QRApiAdapterMock
from core.tests_pytest.utils import (
    create_active_user_in_test_db,
    create_test_company_in_db,
    create_test_vacancy_in_db,
    get_test_file_bytes,
    get_test_image,
    get_test_pdf,
)
from django.contrib.auth.models import AbstractBaseUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.test import APIClient


@dataclass
class CreatedDBData:
    company_1: Company
    company_2: Company
    company_3: Company
    vacancy_1: Vacancy
    vacancy_2: Vacancy
    vacancy_3: Vacancy
    vacancy_4: Vacancy


@pytest.fixture
def pdf_for_test() -> InMemoryUploadedFile:
    return get_test_pdf()


@pytest.fixture
def png_for_test() -> InMemoryUploadedFile:
    return get_test_image()


@pytest.fixture
def png_bytes() -> io.BytesIO:
    return get_test_file_bytes()


@pytest.fixture(autouse=True)
def populate_db(png_for_test: InMemoryUploadedFile, pdf_for_test: InMemoryUploadedFile) -> CreatedDBData:
    company_1 = create_test_company_in_db(company_name='test_company_1', test_file=png_for_test)
    company_2 = create_test_company_in_db(company_name='test_company_2', test_file=png_for_test)
    company_3 = create_test_company_in_db(company_name='test_company_3', test_file=png_for_test)
    vacancy_1 = create_test_vacancy_in_db(
        vacancy_name='Test_vacancy_1',
        company=company_1,
        attachment_file=pdf_for_test,
        min_salary=100,
        max_salary=1000,
        description='vac_1 description',
        employment_formats=['B2B'],
        work_formats=['Freelance', 'Part-time'],
        cities='Minsk',
        tags='python sql',
    )
    vacancy_2 = create_test_vacancy_in_db(
        vacancy_name='Test_vacancy_2', company=company_1, attachment_file=pdf_for_test
    )
    vacancy_3 = create_test_vacancy_in_db(
        vacancy_name='Test_vacancy_3', company=company_2, attachment_file=pdf_for_test
    )
    vacancy_4 = create_test_vacancy_in_db(
        vacancy_name='another_vacancy_1',
        company=company_3,
        attachment_file=pdf_for_test,
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
    return CreatedDBData(
        company_1=company_1,
        company_2=company_2,
        company_3=company_3,
        vacancy_1=vacancy_1,
        vacancy_2=vacancy_2,
        vacancy_3=vacancy_3,
        vacancy_4=vacancy_4,
    )


@pytest.fixture()
def create_users_in_db() -> tuple[AbstractBaseUser, AbstractBaseUser]:
    user_1 = create_active_user_in_test_db(username='test_user_1', email='test_1@test.com', role='candidate')
    user_2 = create_active_user_in_test_db(username='test_user_2', email='test_2@test.com', role='recruiter')
    result: tuple[AbstractBaseUser, AbstractBaseUser] = (user_1, user_2)
    return result


@pytest.fixture
def qr_adapter_mock() -> QRApiAdapterMock:
    return QRApiAdapterMock()


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    client = APIClient()
    yield client
