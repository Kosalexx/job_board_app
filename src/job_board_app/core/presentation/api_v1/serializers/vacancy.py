"""
"Core" app Vacancy API serializers of job_board_app project.
"""

from rest_framework import serializers


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


class CompanyInfoSerializer(serializers.Serializer):
    """Serializes company data from the database related to a specific vacancy."""

    id = serializers.IntegerField()
    name = serializers.CharField()


class LevelInfoSerializer(serializers.Serializer):
    """Serializes level data from the database related to a specific vacancy."""

    id = serializers.IntegerField()
    name = serializers.CharField()


class VacancyInfoSerializer(serializers.Serializer):
    """Serializes vacancy data from the database."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    company = CompanyInfoSerializer()
    level = LevelInfoSerializer()
    experience = serializers.CharField()
    min_salary = serializers.IntegerField()
    max_salary = serializers.IntegerField()


class EmploymentFormatSerializer(serializers.Serializer):
    """Serializes employment_format data from the database."""

    id = serializers.IntegerField()
    name = serializers.CharField()


class WorkFormatSerializer(serializers.Serializer):
    """Serializes work_format data from the database."""

    id = serializers.IntegerField()
    name = serializers.CharField()


class CountrySerializer(serializers.Serializer):
    """Serializes country data from the database."""

    id = serializers.IntegerField()
    name = serializers.CharField()


class CitySerializer(serializers.Serializer):
    """Serializes city data from the database."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    country = CountrySerializer()


class TagsSerializer(serializers.Serializer):
    """Serializes tags data form the database."""

    id = serializers.IntegerField()
    name = serializers.CharField()


class VacancyExtendedInfoSerializer(VacancyInfoSerializer):
    """Serializes extended vacancy data from the database."""

    description = serializers.CharField()
    employment_format = EmploymentFormatSerializer(many=True, read_only=True)
    work_format = WorkFormatSerializer(many=True, read_only=True)
    city = CitySerializer(many=True, read_only=True)
    tags = TagsSerializer(many=True, read_only=True)
