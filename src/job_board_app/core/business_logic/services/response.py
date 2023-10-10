"""
Services and business logic for working responses.
"""

from core.models import ResponseStatus


def get_response_status_by_name(status_name: str) -> ResponseStatus:
    """Gets response status from DB."""

    status: ResponseStatus = ResponseStatus.objects.get(name=status_name.capitalize())
    return status
