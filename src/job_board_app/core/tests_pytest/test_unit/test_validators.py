import pytest
from core.presentation.common.validators import (
    ValidateFileExtensions,
    ValidateFileSize,
    ValidateImageExtensions,
    ValidateMaxAreasCount,
    ValidateMaxTagCount,
    validate_swear_words_in_company_name,
)
from core.tests_pytest.mocks import FileMock


@pytest.mark.django_db
def test_validate_file_size_successfully() -> None:
    """Checks correctness of file size validation when passed valid value."""
    validator = ValidateFileSize(max_size=10_000_000)
    test_file = FileMock(size=5_000_000)

    result = validator(value=test_file)

    assert result == {"status": True}


@pytest.mark.django_db
def test_validate_file_size_validation_failed() -> None:
    """Checks correctness of file size validation when passed invalid value."""

    validator = ValidateFileSize(max_size=10_000_000)
    test_file = FileMock(size=15_000_000)

    result = validator(value=test_file)

    assert result == {"status": False, "message": "Max file size is 10 MB"}


@pytest.mark.django_db
def test_validate_file_extension_successfully() -> None:
    """Checks correctness of file extension validation when passed valid value."""

    validator = ValidateFileExtensions(available_extensions=["pdf"])
    test_file = FileMock(name='test.pdf')

    result = validator(value=test_file)

    assert result == {"status": True}


@pytest.mark.django_db
def test_validate_file_extension_invalid_file_name() -> None:
    """Checks correctness of file extension validation when passed invalid value."""

    validator = ValidateFileExtensions(available_extensions=["pdf"])
    test_file = FileMock(name="test")

    result = validator(value=test_file)

    assert result == {"status": False, "message": "Accept only ['pdf']"}


@pytest.mark.django_db
def test_validate_image_extension_successfully() -> None:
    """Checks correctness of image extension validation when passed valid value."""

    validator = ValidateImageExtensions(available_extensions=["jpg", "jpeg", "png"])
    test_file_1 = FileMock(name="test.jpg")
    test_file_2 = FileMock(name="test.jpeg")
    test_file_3 = FileMock(name="test.png")
    result_1 = validator(value=test_file_1)
    result_2 = validator(value=test_file_2)
    result_3 = validator(value=test_file_3)
    assert result_1 == {"status": True}
    assert result_2 == {"status": True}
    assert result_3, {"status": True}


@pytest.mark.django_db
def test_validate_image_extension_invalid_file_name() -> None:
    """Checks correctness of image extension validation when passed invalid valid value."""

    validator = ValidateImageExtensions(available_extensions=["jpg", "jpeg", "png"])
    test_file = FileMock(name="test")
    result = validator(value=test_file)
    assert result, {"status": False, "message": "Accept only ['jpg', 'jpeg', 'png']"}


@pytest.mark.django_db
def test_validate_max_tag_count_successfully() -> None:
    """Checks correctness of max tag count validation when passed valid value."""

    validator = ValidateMaxTagCount(max_count=3)
    tags = "Python\r\nPostgres"
    result = validator(value=tags)
    assert result == {"status": True}


@pytest.mark.django_db
def test_validate_max_tag_count_validation_failed() -> None:
    """Checks correctness of max tag count validation when passed invalid value."""

    validator = ValidateMaxTagCount(max_count=3)
    tags = "Python\r\nPostgres\r\nHttp\r\nDocker"
    result = validator(value=tags)
    assert result == {"status": False, "message": "Max number of tags is 3"}


@pytest.mark.django_db
def test_validate_max_areas_count_successfully() -> None:
    """Checks correctness of max areas count validation when passed valid value."""

    validator = ValidateMaxAreasCount(max_count=3)
    tags = "Web\r\nAI"
    result = validator(value=tags)
    assert result == {"status": True}
    tags = "Area1 area2 area3"
    result = validator(value=tags)
    assert result == {"status": True}


@pytest.mark.django_db
def test_validate_max_areas_count_validation_failed() -> None:
    """Checks correctness of max areas count validation when passed invalid value."""

    validator = ValidateMaxAreasCount(max_count=3)
    tags = "Web\r\nAI\r\nArea_3\r\nArea_4"
    result = validator(value=tags)
    assert result == {"status": False, "message": "Max number of business areas is 3"}


@pytest.mark.django_db
def test_validate_swear_words_in_company_name_successfully() -> None:
    """Checks correctness swear words in company name validation when passed valid value."""

    company_name = 'Company name'
    result = validate_swear_words_in_company_name(value=company_name)
    assert {"status": True} == result


@pytest.mark.django_db
def test_validate_swear_words_in_company_name_failed() -> None:
    """Checks correctness swear words in company name validation when passed invalid value."""

    company_name = 'Fucking Company name'
    result = validate_swear_words_in_company_name(value=company_name)
    assert {"status": False, "message": "Company name contains swear word."} == result
