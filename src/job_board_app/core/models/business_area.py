"""
"Core" app Business_area model of job_board_app project.
"""

from django.db import models

from .base import BaseModel


class BusinessArea(BaseModel):
    """Describes the fields and attributes of the Business_area model in the database."""

    name = models.CharField(unique=True, max_length=100)

    class Meta:
        """Describes class metadata."""

        db_table = "business_areas"
