"""
"Core" app Position model of job_board_app project.
"""

from django.db import models

from .base import BaseModel


class Position(BaseModel):
    """Describes the fields and attributes of the Position model in the database."""

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        """Describes class metadata."""

        db_table = "positions"
