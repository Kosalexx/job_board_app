"""
"Core" app Company forms of job_board_app project.
"""

from core.models import Country
from core.presentation.validators import (
    ValidateFileSize,
    ValidateImageExtensions,
    ValidateMaxAreasCount,
    validate_swear_words_in_company_name,
)
from django import forms

COUNTRIES = [(value.name, value.name) for value in Country.objects.all()]


class AddCompanyForm(forms.Form):
    """Form for adding a new company."""

    name = forms.CharField(
        label="Company name", max_length="30", strip=True, validators=[validate_swear_words_in_company_name]
    )
    staff = forms.IntegerField(label="Employees number", min_value=1)
    business_area = forms.CharField(
        label="Business areas", widget=forms.Textarea, validators=[ValidateMaxAreasCount(max_count=5)]
    )


class CompanyProfileForm(forms.Form):
    """Form for adding a new company profile."""

    logo = forms.ImageField(
        label='Logo',
        allow_empty_file=False,
        required=False,
        validators=[ValidateImageExtensions(['png', 'jpeg']), ValidateFileSize(max_size=5_000_000)],
    )
    email = forms.EmailField(label='Email', required=True)
    founding_year = forms.IntegerField(min_value=1800, required=True)
    description = forms.CharField(label='Description', widget=forms.Textarea, strip=True, required=True)
    phone = forms.CharField(label='Phone', max_length=20, required=True)
    website_link = forms.CharField(max_length=100, required=True)
    linkedin_link = forms.CharField(max_length=100, required=False)
    github_link = forms.CharField(max_length=100, required=False)
    twitter_link = forms.CharField(max_length=100, required=False)


class AddAddressFrom(forms.Form):
    """Form for adding a new address."""

    country = forms.ChoiceField(label='Country', choices=COUNTRIES, required=True)
    city = forms.CharField(max_length=100, required=True)
    street_name = forms.CharField(max_length=100, required=True)
    home_number = forms.IntegerField(min_value=1, required=True)
    office_number = forms.IntegerField(min_value=1, required=False)
