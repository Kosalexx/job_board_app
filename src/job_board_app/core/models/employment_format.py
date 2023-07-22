"""
"Core" app Employment_format model of job_board_app project.
"""

from django.db import models

from .base import BaseModel


class EmploymentFormat(BaseModel):
    """Describes the fields and attributes of the Employment_format model in the database."""

    name = models.CharField(max_length=30, unique=True)

    class Meta:
        """Describes class metadata."""

        db_table = 'employment_formats'
