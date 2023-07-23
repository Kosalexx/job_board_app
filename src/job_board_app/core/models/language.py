"""
"Core" app Language models of job_board_app project.
"""

from django.db import models

from .base import BaseModel


class Language(BaseModel):
    """Describes the fields and attributes of the Language model in the database."""

    name = models.CharField(max_length=30, unique=True)

    class Meta:
        """Describes class metadata."""

        db_table = 'languages'


class LanguageLevel(BaseModel):
    """Describes the fields and attributes of the Language_level model in the database."""

    name = models.CharField(max_length=30, unique=True)

    class Meta:
        """Describes class metadata."""

        db_table = 'language_levels'
