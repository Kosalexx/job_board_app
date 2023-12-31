"""
"Core" app Company forms of job_board_app project.
"""
from typing import Any

from core.presentation.common.validators import (
    ValidateFileSize,
    ValidateImageExtensions,
    ValidateMaxAreasCount,
    validate_swear_words_in_company_name,
)
from core.presentation.web.validators import ValidateWebData
from django import forms


class AddCompanyForm(forms.Form):
    """Form for adding a new company."""

    name = forms.CharField(
        label="Company name",
        max_length="30",
        strip=True,
        validators=[ValidateWebData(validate_swear_words_in_company_name)],
    )
    staff = forms.IntegerField(label="Employees number", min_value=1)
    business_area = forms.CharField(
        label="Business areas", widget=forms.Textarea, validators=[ValidateWebData(ValidateMaxAreasCount(max_count=5))]
    )


class CompanyProfileForm(forms.Form):
    """Form for adding a new company profile."""

    logo = forms.ImageField(
        label='Logo',
        allow_empty_file=False,
        required=False,
        validators=[
            ValidateWebData(ValidateImageExtensions(['png', 'jpeg'])),
            ValidateWebData(ValidateFileSize(max_size=5_000_000)),
        ],
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

    country = forms.ChoiceField(label='Country', required=True)
    city = forms.CharField(max_length=100, required=True)
    street_name = forms.CharField(max_length=100, required=True)
    home_number = forms.IntegerField(min_value=1, required=True)
    office_number = forms.IntegerField(min_value=1, required=False)

    def __init__(self, countries: list[tuple[str, str]], *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["country"].choices = countries
