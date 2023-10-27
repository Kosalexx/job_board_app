"""
Custom exceptions, that uses in custom validators.
"""


class CompanyNotExistsError(Exception):
    """Exception that raises when company with entered name does not exist in the database."""


class CompanyProfileNotExistsError(Exception):
    """Exception that raises when company profile with entered name does not exist in the database."""


class ConfirmationCodeNotExistError(Exception):
    """Exception that raises when confirmation code doesn't exist."""


class ConfirmationCodeExpiredError(Exception):
    """Exception that raises when confirmation code already expired."""


class InvalidAuthCredentialsError(Exception):
    """Exception that raises when auth credentials are invalid."""


class UserAlreadyExistsError(Exception):
    """Exception that raises when user already exist in the database."""


class VacancyNotExistsError(Exception):
    """Exception that raises when vacancy with entered name(or id) does not exist in the database."""


class CompanyAlreadyExistsError(Exception):
    """Exception that raises when company with passed name already exists."""


class CountryNotExistError(Exception):
    """Exception that raises when country with passed name does not exist in the database."""


class EmploymentFormatNotExistError(Exception):
    """Exception that raises when Employment format with passed name does not exist in the database."""


class WorkFormatNotExistError(Exception):
    """Exception that raises when Work format with passed name does not exist in the database."""


class QRCodeServiceUnavailable(Exception):
    """Exception that raises when QR Code Service is unavailable."""
