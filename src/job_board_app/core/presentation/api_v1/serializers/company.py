"""
"Core" app Company API serializers of job_board_app project.
"""
from core.presentation.api_v1.validators import ValidateAPIData
from core.presentation.common.validators import (
    ValidateFileExtensions,
    ValidateFileSize,
    ValidateMaxAreasCount,
    validate_swear_words_in_company_name,
)
from rest_framework import serializers

from .common import AddressSerializer


class CompanyInfoSerializer(serializers.Serializer):
    """Serializes data about companies from the database."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    staff = serializers.IntegerField()
    vacancy__count = serializers.IntegerField()


class CompanyProfileSerializer(serializers.Serializer):
    """Serializes data about company profile from the database."""

    logo = serializers.CharField()
    email = serializers.CharField()
    founding_year = serializers.IntegerField()
    description = serializers.CharField()
    phone = serializers.CharField()
    website_link = serializers.CharField()
    linkedin_link = serializers.CharField()
    github_link = serializers.CharField()
    twitter_link = serializers.CharField()
    address = AddressSerializer()


class BusinessAreaSerializer(serializers.Serializer):
    """Serializes data about business areas from the database."""

    id = serializers.IntegerField()
    name = serializers.CharField()


class CompanyExtendedInfoSerializer(CompanyInfoSerializer):
    """Serializes extended data about companies from the database."""

    business_area = BusinessAreaSerializer(many=True, read_only=True)
    company_profile = CompanyProfileSerializer()


class AddCompanySerializer(serializers.Serializer):
    """Serializes data about new company."""

    name = serializers.CharField(
        max_length=30,
        trim_whitespace=True,
        validators=[ValidateAPIData(validate_swear_words_in_company_name)],
        required=True,
    )
    staff = serializers.IntegerField(min_value=1, required=True)
    business_area = serializers.CharField(
        validators=[ValidateAPIData(ValidateMaxAreasCount(max_count=5))], required=True
    )
    logo = serializers.ImageField(
        allow_empty_file=False,
        validators=[
            ValidateAPIData(ValidateFileExtensions(["png", "jpg", "jpeg"])),
            ValidateAPIData(ValidateFileSize(max_size=5_000_000)),
        ],
        required=False,
    )
    email = serializers.EmailField(allow_blank=False, required=True)
    founding_year = serializers.IntegerField(min_value=1, required=True)
    description = serializers.CharField(trim_whitespace=True, max_length=900, required=False)
    phone = serializers.CharField(max_length=20, allow_blank=False, allow_null=False, required=True)
    website_link = serializers.CharField(max_length=100, allow_blank=False, allow_null=False, required=True)
    linkedin_link = serializers.CharField(max_length=100, allow_blank=True, allow_null=True, required=False)
    github_link = serializers.CharField(max_length=100, allow_blank=True, allow_null=True, required=False)
    twitter_link = serializers.CharField(max_length=100, allow_blank=True, allow_null=True, required=False)
    country = serializers.CharField(allow_blank=False, allow_null=False, required=True)
    city = serializers.CharField(max_length=100, allow_blank=False, allow_null=False, required=True)
    street_name = serializers.CharField(max_length=100, allow_blank=False, allow_null=False, required=True)
    home_number = serializers.IntegerField(min_value=1, required=True)
    office_number = serializers.IntegerField(min_value=1, required=False)


class AddCompanyResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    company_id = serializers.IntegerField()
