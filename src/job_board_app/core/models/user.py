"""
"Core" app User models of job_board_app project.
"""

from django.db import models

from .base import BaseModel


class UsersProfile(BaseModel):
    """Describes the fields and attributes of the Users_profile model in the database."""

    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    age = models.PositiveSmallIntegerField()
    city = models.ForeignKey(
        to="City", on_delete=models.CASCADE, related_name='users_profiles', related_query_name='users_profile'
    )
    experience_description = models.CharField(max_length=800)
    linkedin_link = models.CharField(max_length=100, blank=True)
    github_link = models.CharField(max_length=100, blank=True)
    work_experience = models.IntegerField(blank=True)
    level = models.ForeignKey(
        to='Level', on_delete=models.CASCADE, related_name='users_profiles', related_query_name='users_profile'
    )
    min_salary = models.PositiveIntegerField(null=True)
    max_salary = models.PositiveIntegerField(null=True)

    class Meta:
        """Describes class metadata."""

        db_table = 'users_profiles'


class User(BaseModel):
    """Describes the fields and attributes of the User model in the database."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo_link = models.CharField(max_length=100, unique=True, blank=True)
    summary_link = models.CharField(max_length=100, unique=True)
    work_status = models.ForeignKey(
        to='WorkStatus', on_delete=models.CASCADE, related_name='users', related_query_name='user'
    )
    profile = models.OneToOneField(
        to='UsersProfile', on_delete=models.CASCADE, related_name='users', related_query_name='user'
    )
    email = models.EmailField()
    tags = models.ManyToManyField(to='Tag', related_name='users', related_query_name='user', db_table='users_tags')
    employment_format = models.ManyToManyField(
        to="EmploymentFormat", related_name='users', related_query_name='user', db_table='users_employment_formats'
    )
    work_format = models.ManyToManyField(
        to="WorkFormat", related_name='users', related_query_name='user', db_table='users_work_formats'
    )
    user_language = models.ManyToManyField(to="Language", through="UsersLanguages")

    class Meta:
        """Describes class metadata."""

        db_table = 'users'


class UsersLanguages(BaseModel):
    """Describes the fields and attributes of the User_language model in the database."""

    user = models.ForeignKey(
        to="User", on_delete=models.CASCADE, related_name='users_languages', related_query_name='users_language'
    )
    language = models.ForeignKey(
        to="Language", on_delete=models.CASCADE, related_name='users_languages', related_query_name='users_language'
    )
    language_level = models.ForeignKey(
        to='LanguageLevel',
        on_delete=models.CASCADE,
        related_name='users_languages',
        related_query_name='users_language',
    )

    class Meta:
        """Describes class metadata."""

        db_table = "users_languages"
