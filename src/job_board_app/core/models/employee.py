"""
"Core" app Employee model of job_board_app project.
"""

from django.db import models

from .base import BaseModel


class Employee(BaseModel):
    """Describes the fields and attributes of the Employee model in the database."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.ForeignKey(
        to="Company", on_delete=models.CASCADE, related_name='employees', related_query_name='employee'
    )
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    login = (models.CharField(max_length=50, unique=True),)
    password = models.CharField(max_length=50)
    city = models.ForeignKey(
        to="City", on_delete=models.CASCADE, related_name='employees', related_query_name='employee'
    )
    photo_link = models.CharField(blank=True)
    position = models.ManyToManyField(to="Position", related_name='employees', db_table='employee_positions')

    class Meta:
        """Describes class metadata."""

        db_table = "employees"
