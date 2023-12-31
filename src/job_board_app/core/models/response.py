"""
"Core" app Response models of job_board_app project.
"""

from django.contrib.auth import get_user_model
from django.db import models

from .base import BaseModel


def response_directory_path(instance: "Response", filename: str) -> str:
    """Provides a path to directory with files of specific responce."""

    return f'response_attachments/user_{instance.user.pk}/vacancy_{instance.vacancy.pk}/{filename}'


class ResponseStatus(BaseModel):
    """Describes the fields and attributes of the Response_status model in the database."""

    name = models.CharField(max_length=30, unique=True)

    class Meta:
        """Describes class metadata."""

        db_table = "response_statuses"


class Response(BaseModel):
    """Describes the fields and attributes of the Response model in the database."""

    user = models.ForeignKey(
        to=get_user_model(), on_delete=models.CASCADE, related_name='responses', related_query_name='response'
    )
    vacancy = models.ForeignKey(
        to="Vacancy", on_delete=models.CASCADE, related_name='responses', related_query_name='response'
    )
    cover_note = models.CharField(max_length=500)
    cv = models.FileField(upload_to=response_directory_path, null=True)
    response_status = models.ForeignKey(
        to="ResponseStatus", on_delete=models.CASCADE, related_name='responses', related_query_name='response'
    )

    class Meta:
        """Describes class metadata."""

        db_table = "responses"
