"""
"Core" app Tag model of job_board_app project.
"""

from django.db import models

from .base import BaseModel


class Tag(BaseModel):
    """Describes the fields and attributes of the Tag model in the database."""

    name = models.CharField(max_length=30)

    class Meta:
        """Describes class metadata."""

        db_table = "tags"
