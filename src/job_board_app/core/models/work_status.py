"""
"Core" app Work_status model of job_board_app project.
"""

from django.db import models

from .base import BaseModel


class WorkStatus(BaseModel):
    """Describes the fields and attributes of the Work_status model in the database."""

    name = models.CharField(max_length=30, unique=True)

    class Meta:
        """Describes class metadata."""

        db_table = 'work_statuses'
