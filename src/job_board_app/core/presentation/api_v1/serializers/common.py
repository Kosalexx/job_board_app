"""
"Core" app common API serializers of job_board_app project.
"""
from rest_framework import serializers


class LevelInfoSerializer(serializers.Serializer):
    """Serializes level data from the database related to a specific vacancy."""

    id = serializers.IntegerField()
    name = serializers.CharField()


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


class AddressSerializer(serializers.Serializer):
    """Serializes data about address from the database."""

    id = serializers.IntegerField()
    street_name = serializers.CharField()
    home_number = serializers.IntegerField()
    office_number = serializers.IntegerField()
    city = CitySerializer()
