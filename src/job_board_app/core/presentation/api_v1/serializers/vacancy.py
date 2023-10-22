"""
"Core" app Vacancy API serializers of job_board_app project.
"""

from core.presentation.api_v1.validators import ValidateAPIData
from core.presentation.common.validators import ValidateFileExtensions, ValidateFileSize
from rest_framework import serializers

from .common import (
    CitySerializer,
    EmploymentFormatSerializer,
    LevelInfoSerializer,
    TagsSerializer,
    WorkFormatSerializer,
)


class SearchVacancySerializer(serializers.Serializer):
    """Validates and serializes data from the search vacancy filter."""

    name = serializers.CharField(max_length=30, trim_whitespace=True, required=False, default="")
    company_name = serializers.CharField(max_length=30, trim_whitespace=True, required=False, default="")
    level = serializers.CharField(max_length=30, trim_whitespace=True, required=False, default="")
    experience = serializers.CharField(max_length=30, trim_whitespace=True, required=False, default="")
    min_salary = serializers.IntegerField(min_value=0, required=False, default=None)
    max_salary = serializers.IntegerField(min_value=0, required=False, default=None)
    tag = serializers.CharField(required=False, default="")
    level = serializers.CharField(max_length=30, trim_whitespace=True, required=False, default="")
    employment_format = serializers.ListField(
        child=serializers.CharField(max_length=30, trim_whitespace=True, required=False, default=""),
        required=False,
        default=[],
    )
    work_format = serializers.ListField(
        child=serializers.CharField(max_length=30, trim_whitespace=True, required=False, default=""),
        allow_empty=True,
        default=[],
    )
    country = serializers.CharField(max_length=30, trim_whitespace=True, required=False, default="")
    city = serializers.CharField(max_length=30, trim_whitespace=True, required=False, default="")


class VacancyCompanyInfoSerializer(serializers.Serializer):
    """Serializes company data from the database related to a specific vacancy."""

    id = serializers.IntegerField()
    name = serializers.CharField()


class VacancyInfoSerializer(serializers.Serializer):
    """Serializes vacancy data from the database."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    company = VacancyCompanyInfoSerializer()
    level = LevelInfoSerializer()
    experience = serializers.CharField()
    min_salary = serializers.IntegerField()
    max_salary = serializers.IntegerField()


class VacancyExtendedInfoSerializer(VacancyInfoSerializer):
    """Serializes extended vacancy data from the database."""

    description = serializers.CharField()
    employment_format = EmploymentFormatSerializer(many=True, read_only=True)
    work_format = WorkFormatSerializer(many=True, read_only=True)
    city = CitySerializer(many=True, read_only=True)
    tags = TagsSerializer(many=True, read_only=True)
    attachment = serializers.CharField()


class AddVacancySerializer(serializers.Serializer):
    """Serializes and validates data about added vacancy."""

    name = serializers.CharField(max_length=30, trim_whitespace=True)
    company_name = serializers.CharField(max_length=30, trim_whitespace=True)
    level = serializers.CharField(max_length=30, trim_whitespace=True)
    experience = serializers.CharField(max_length=30, trim_whitespace=True)
    min_salary = serializers.IntegerField(min_value=0, required=False, default=None)
    max_salary = serializers.IntegerField(min_value=0, required=False, default=None)
    description = serializers.CharField(trim_whitespace=True)
    employment_format = serializers.ListField(child=serializers.CharField(max_length=30, trim_whitespace=True))
    work_format = serializers.ListField(child=serializers.CharField(max_length=30, trim_whitespace=True))
    country = serializers.CharField(max_length=30, trim_whitespace=True)
    city = serializers.CharField(max_length=30, trim_whitespace=True)
    tags = serializers.CharField(trim_whitespace=True)
    attachment = serializers.FileField(
        allow_empty_file=False,
        validators=[
            ValidateAPIData(ValidateFileExtensions(["pdf"])),
            ValidateAPIData(ValidateFileSize(max_size=5_000_000)),
        ],
        required=False,
    )
