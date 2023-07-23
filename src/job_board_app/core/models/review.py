"""
"Core" app Review model of job_board_app project.
"""

from django.db import models

from .base import BaseModel


class Review(BaseModel):
    """Describes the fields and attributes of the Review model in the database."""

    company = models.ForeignKey(
        to="Company", on_delete=models.CASCADE, related_name='reviews', related_query_name='review'
    )
    user = models.ForeignKey(to='User', on_delete=models.CASCADE, related_name='reviews', related_query_name='review')
    text = models.CharField(max_length=800)
    likes_counter = models.PositiveIntegerField(default=0)
    dislike_counter = models.PositiveIntegerField(default=0)

    class Meta:
        """Describes class metadata."""

        db_table = "reviews"
