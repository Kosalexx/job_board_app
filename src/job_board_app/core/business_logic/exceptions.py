"""
Custom exceptions, that uses in custom validators.
"""


class CompanyNotExists(Exception):
    """Exception that raises when company with entered name does not exist in the database."""
