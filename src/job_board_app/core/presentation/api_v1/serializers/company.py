from rest_framework import serializers


class CompaniesListSerializer(serializers.Serializer):
    """Serializes data about companies from the database."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    staff = serializers.ImageField()
    vacancy__count = serializers.IntegerField()
