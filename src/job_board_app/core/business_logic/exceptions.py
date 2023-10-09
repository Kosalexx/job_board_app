"""
Custom exceptions, that uses in custom validators.
"""


class CompanyNotExistsError(Exception):
    """Exception that raises when company with entered name does not exist in the database."""


class ConfirmationCodeNotExistError(Exception):
    """Exception that raises when confirmation code doesn't exist."""


class ConfirmationCodeExpiredError(Exception):
    """Exception that raises when confirmation code already expired."""


class InvalidAuthCredentialsError(Exception):
    """Exception that raises when auth credentials are invalid."""


class UserAlreadyExistsError(Exception):
    """Exception that raises when user already exist in the database."""
