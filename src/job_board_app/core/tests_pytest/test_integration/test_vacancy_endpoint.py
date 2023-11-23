import pytest
from core.tests_pytest.conftest import CreatedDBData
from dirty_equals import IsListOrTuple, IsPositiveInt, IsStr
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_get_all_vacancies_successfully(api_client: APIClient) -> None:
    response = api_client.get("/api/v1/vacancies/")

    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        "count": IsPositiveInt,
        "next": None,
        "previous": None,
        "results": IsListOrTuple(
            {
                "company": {"id": IsPositiveInt, "name": IsStr},
                "id": IsPositiveInt,
                "name": IsStr,
                "level": {"id": IsPositiveInt, "name": IsStr},
                "experience": IsStr,
                "min_salary": IsPositiveInt,
                "max_salary": IsPositiveInt,
            },
            length=4,
        ),
    }


@pytest.mark.django_db
def test_get_all_vacancies_successfully_search_by_name(api_client: APIClient) -> None:
    response = api_client.get("/api/v1/vacancies/?name=test_vacancy_1")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        "count": IsPositiveInt,
        "next": None,
        "previous": None,
        "results": IsListOrTuple(
            {
                "company": {"id": IsPositiveInt, "name": IsStr},
                "experience": IsStr,
                "id": IsPositiveInt,
                "level": {"id": IsPositiveInt, "name": IsStr},
                "name": IsStr,
                "min_salary": IsPositiveInt,
                "max_salary": IsPositiveInt,
            },
            length=1,
        ),
    }
    assert response_data["results"][0]["name"] == "Test_vacancy_1"


@pytest.mark.django_db
def test_get_all_vacancies_successfully_search_by_max_salary(api_client: APIClient) -> None:
    response = api_client.get("/api/v1/vacancies/?max_salary=4000")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        "count": IsPositiveInt,
        "next": None,
        "previous": None,
        "results": IsListOrTuple(
            {
                "id": IsPositiveInt,
                "name": IsStr,
                "company": {"id": IsPositiveInt, "name": IsStr},
                "level": {"id": IsPositiveInt, "name": IsStr},
                "experience": IsStr,
                "min_salary": IsPositiveInt,
                "max_salary": IsPositiveInt,
            },
            length=1,
        ),
    }
    assert response_data["results"][0]["name"] == "Test_vacancy_1"
    assert response_data["results"][0]["max_salary"] <= 4000

    response = api_client.get("/api/v1/vacancies/?max_salary=6000")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        "count": IsPositiveInt,
        "next": None,
        "previous": None,
        "results": IsListOrTuple(
            {
                "id": IsPositiveInt,
                "name": IsStr,
                "company": {"id": IsPositiveInt, "name": IsStr},
                "level": {"id": IsPositiveInt, "name": IsStr},
                "experience": IsStr,
                "min_salary": IsPositiveInt,
                "max_salary": IsPositiveInt,
            },
            length=2,
        ),
    }
    assert response_data["results"][1]["name"] == "Test_vacancy_1"
    assert response_data["results"][0]["name"] == "another_vacancy_1"
    assert response_data["results"][0]["max_salary"] <= 6000
    assert response_data["results"][1]["max_salary"] <= 6000


@pytest.mark.django_db
def test_get_vacancy_by_id_successfully(api_client: APIClient, populate_db: CreatedDBData) -> None:
    vacancy_id = populate_db.vacancy_1.pk

    response = api_client.get(f"/api/v1/vacancies/{vacancy_id}/")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        "id": IsPositiveInt,
        "name": IsStr,
        "company": {"id": IsPositiveInt, "name": IsStr},
        "level": {"id": IsPositiveInt, "name": IsStr},
        "experience": IsStr,
        "description": IsStr,
        "min_salary": IsPositiveInt,
        "max_salary": IsPositiveInt,
        "tags": IsListOrTuple({"id": IsPositiveInt, "name": IsStr}, length=...),
        "employment_format": IsListOrTuple({"id": IsPositiveInt, "name": IsStr}, length=...),
        "work_format": IsListOrTuple({"id": IsPositiveInt, "name": IsStr}, length=...),
        "city": IsListOrTuple(
            {"id": IsPositiveInt, "name": IsStr, "country": {"id": IsPositiveInt, "name": IsStr}}, length=...
        ),
        "attachment": IsStr,
        "qr_code": IsStr,
    }
    assert response_data["name"] == "Test_vacancy_1"


@pytest.mark.django_db
def test_get_vacancy_by_invalid_id(api_client: APIClient) -> None:
    vacancy_id = 1248324234
    response = api_client.get(f"/api/v1/vacancies/{vacancy_id}/")
    response_data = response.json()
    assert response.status_code == 404
    assert response_data["message"] == "Vacancy with provided id doesn't exist."
