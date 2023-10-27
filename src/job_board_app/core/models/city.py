"""
"Core" app City model of job_board_app project.
"""

from django.db import models

from .base import BaseModel


class City(BaseModel):
    """Describes the fields and attributes of the City model in the database."""

    name = models.CharField(max_length=30)
    country = models.ForeignKey(
        to='Country', on_delete=models.CASCADE, related_name='cities', related_query_name='city'
    )

    class Meta:
        """Describes class metadata."""

        db_table = 'cities'
