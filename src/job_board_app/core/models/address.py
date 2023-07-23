"""
"Core" app Address model of job_board_app project.
"""

from django.db import models

from .base import BaseModel


class Address(BaseModel):
    """Describes the fields and attributes of the Address model in the database."""

    street_name = models.CharField(max_length=30)
    home_number = models.PositiveSmallIntegerField()
    office_number = models.PositiveSmallIntegerField(blank=False)
    city = models.ForeignKey(
        to='City', on_delete=models.CASCADE, related_name='addresses', related_query_name='address'
    )

    class Meta:
        """Describes class metadata."""

        db_table = 'addresses'
