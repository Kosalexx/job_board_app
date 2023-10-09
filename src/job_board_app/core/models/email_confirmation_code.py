"""
"Core" app EmailConfirmationCodes model of job_board_app project.
"""
from django.contrib.auth import get_user_model
from django.db import models

from .base import BaseModel


class EmailConfirmationCodes(BaseModel):
    """Describes the fields and attributes of the Country model in the database."""

    code = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='confirmation_codes')
    expiration = models.PositiveIntegerField()

    class Meta:
        """Describes class metadata."""

        db_table = "email_confirmation_codes"
