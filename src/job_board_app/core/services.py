"""
Services and business logic for "core" app job_board_app project.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Company:
    """A dataclass for storing and transmitting data about a company."""

    name: str
    employees_number: int
    vacancies_counter: int = 0
    id: int | None = None  # noqa: A003 pylint: disable=C0103
    reviews_counter: int = 0


@dataclass
class Vacancy:
    """A dataclass for storing and transmitting data about a vacancy."""

    name: str
    company: Company
    level: str
    experience: str
    min_salary: int | None
    max_salary: int | None
    id: int | None = None  # noqa: A003 pylint: disable=C0103


@dataclass
class Profile:
    """A dataclass for storing and transmitting data about a profile."""

    first_name: str
    last_name: str
    email: str
    phone: str
    age: int
    gender: str
    city: str
    country: str
    years_of_experience: int
    experience_description: str
    work_status: str
    linkedin_link: str | None = None
    github_link: str | None = None
    id: int | None = None  # noqa: A003 pylint: disable=C0103


@dataclass
class User:
    """A dataclass for storing and transmitting data about a profile."""

    user_name: str
    password: str
    email: str
    id: int | None = None  # noqa: A003 pylint: disable=C0103


@dataclass
class Review:
    """A dataclass for storing and transmitting data about a review."""

    company: Company
    text: str
    user_name: str
    creation_datetime: str
    update_datetime: str
    like_counter: int = 0
    dislike_counter: int = 0
    id: int | None = None  # noqa: A003 pylint: disable=C0103


@dataclass
class Response:
    """A dataclass for storing and transmitting data about a response."""

    user: User
    vacancy: Vacancy
    cover_note: str
    user_phone: str


class CompanyDuplicateNameError(Exception):
    """Exception that is caused if a company with entered name already exist."""


class CompanyNotExistError(Exception):
    """Exception that is caused if a company with entered name doesn't exist in database."""


class VacancyNotExistError(Exception):
    """Exception that is caused if a company with entered name doesn't exist in database."""


class BaseStorage:  # pylint: disable=too-few-public-methods
    """Base storage class for storing and work with Vacancies or Companies data."""

    ID_COUNT = 0

    def update_counter(self) -> int:
        """Updates ID counter by 1."""
        self.ID_COUNT += 1  # pylint: disable=C0103
        return self.ID_COUNT  # pylint: disable=C0103


class CompanyStorage(BaseStorage):
    """Company storage class for storing and work with Companies data."""

    def __init__(self) -> None:
        self._companies: list[Company] = []

    def _validate_company(self, company_to_add: Company) -> None:
        """Validates company data based on company.name.

        :param company_to_add: Company DTO
        :type company_to_add: class Company

        :raises CompanyDuplicateNameError: if company.name.lower() already exist in database

        :return type: None
        """
        for company in self._companies:
            if company.name.lower() == company_to_add.name.lower():
                raise CompanyDuplicateNameError

    def add_company(self, company_to_add: Company) -> None:
        """Add company data to the database.

        :param company_to_add: Company DTO
        :type company_to_add: class Company

        :return type: None
        """
        self._validate_company(company_to_add=company_to_add)
        primary_key = self.update_counter()
        company_to_add.id = primary_key
        self._companies.append(company_to_add)

    def get_all_companies(self) -> list[Company]:
        """Returns list of all companies in the database.

        :return type: list[Company]
        :return: list of Company DTO with data about all companies in database
        """
        return self._companies

    def get_company_by_name(self, company_name: str) -> Company:
        """Returns company DTO based on entered company name.

        :param company_name: name of searched company
        :type company_name: str

        :raises CompanyNotExistError: if company not exist in database

        :return type: Optional[Company]
        :return: Company DTO with data about searched company
        """
        for company in self._companies:
            if company.name.lower() == company_name.lower():
                return company
        raise CompanyNotExistError

    def get_company_by_id(self, company_id: int) -> Company:
        """Returns company DTO by entered company id.

        :param company_id: id of searched company
        :type company_id: int

        :raises CompanyNotExistError: if company not exist in database

        :return type: Optional[Company]
        :return: Company DTO with data about searched company
        """
        for company in self._companies:
            if company.id == company_id:
                return company
        raise CompanyNotExistError


class VacancyStorage(BaseStorage):
    """Vacancy storage class for storing and work with vacancies data."""

    def __init__(self, company_storage: CompanyStorage) -> None:
        self._vacancies: list[Vacancy] = []
        self._company_storage = company_storage

    def add_vacancy(self, vacancy_to_add: Vacancy) -> None:
        """Add vacancy data to the database.

        :param vacancy_to_add: Vacancy DTO
        :type vacancy_to_add: class Vacancy

        :return type: None
        """
        company = self._company_storage.get_company_by_name(company_name=vacancy_to_add.company.name)
        primary_key = self.update_counter()
        vacancy_to_add.id = primary_key
        self._vacancies.append(vacancy_to_add)
        company.vacancies_counter += 1

    def get_all_vacancies(self) -> list[Vacancy]:
        """Returns list of all vacancies in the database.

        :return type: list[Vacancy]
        :return: list of Vacancy DTO with data about all vacancies in database
        """
        return self._vacancies

    def get_vacancy_by_company(self, company_name: str) -> list[Vacancy]:
        """Returns list of vacancies by company name.

        :param company_name: name of company
        :type company_name: str

        :return type: list[Vacancy]
        :return: list of vacancies by company name
        """
        vacancies_list: list = []
        for vacancy in self._vacancies:
            if vacancy.company.name.lower() == company_name.lower():
                vacancies_list.append(vacancy)
        return vacancies_list

    def get_vacancy_by_id(self, vacancy_id: int) -> Vacancy:
        """Returns vacancy DTO by entered vacancy_id.

        :param vacancy_id: id of searched vacancy
        :type vacancy_id: int

        :raises VacancyNotExistError: if vacancy not exist in database

        :return type: Optional[Vacancy]
        :return: Vacancy DTO with info about searched vacancy
        """
        for vacancy in self._vacancies:
            if vacancy.id == vacancy_id:
                return vacancy
        raise VacancyNotExistError


class UserStorage(BaseStorage):
    """User storage class for storing and work with user data."""

    def __init__(self) -> None:
        self._user: list[User] = []
        self._profile: list[Profile] = []

    def add_user(self, user_to_add: User) -> None:
        """Add user data to the database.

        :param user_to_add: User DTO
        :type user_to_add: class User

        :return type: None
        """
        primary_key = self.update_counter()
        user_to_add.id = primary_key
        self._user.append(user_to_add)

    def add_profile(self, profile_to_add: Profile) -> None:
        """Add profile data to the database.

        :param profile_to_add: Profile DTO
        :type profile_to_add: class Profile

        :return type: None
        """
        profile_to_add.id = self._user[0].id
        self._profile.append(profile_to_add)


class ReviewStorage(BaseStorage):
    """Review storage class for storing and work with reviews data."""

    def __init__(self, company_storage: CompanyStorage) -> None:
        self._reviews: list[Review] = []
        self._company_storage = company_storage

    def add_review(self, review_to_add: Review) -> None:
        """Add review data to the database.

        :param review_to_add: Review DTO
        :type review_to_add: class Review

        :return type: None
        """
        company = self._company_storage.get_company_by_name(company_name=review_to_add.company.name)
        primary_key = self.update_counter()
        review_to_add.id = primary_key
        self._reviews.append(review_to_add)
        company.reviews_counter += 1

    def get_all_reviews_by_company_id(self, company_id: int) -> list[Review]:
        """Returns list of all review by the entered company id.

        :return type: list[Company]
        :return: list of Company DTO with reviews about company with entered id
        """
        reviews_list: list = []
        for review in self._reviews:
            if review.company.id == company_id:
                reviews_list.append(review)
        return reviews_list
