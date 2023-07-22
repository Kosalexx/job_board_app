"""
"Core" app Country model of job_board_app project.
"""

from django.db import models

from .base import BaseModel


class Country(BaseModel):
    """Describes the fields and attributes of the Country model in the database."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        """Describes class metadata."""

        db_table = 'countries'
