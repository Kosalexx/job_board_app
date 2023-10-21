"""
"Core" app Company API serializers of job_board_app project.
"""
from rest_framework import serializers

from .common import AddressSerializer


class CompaniesListSerializer(serializers.Serializer):
    """Serializes data about companies from the database."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    staff = serializers.ImageField()
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


class CompanyExtendedInfoSerializer(CompaniesListSerializer):
    """Serializes extended data about companies from the database."""

    business_area = BusinessAreaSerializer(many=True, read_only=True)
    company_profile = CompanyProfileSerializer()
