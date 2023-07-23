"""
"Core" app Vacancy forms of job_board_app project.
"""

from core.models import Country, EmploymentFormat, Level, WorkFormat
from core.presentation.validators import (
    ValidateFileExtensions,
    ValidateFileSize,
    ValidateMaxTagCount,
)
from django import forms

LEVELS = [(level.name, level.name) for level in Level.objects.all()]
EMPLOYMENT_FORMATS = [(value.name, value.name) for value in EmploymentFormat.objects.all()]
WORK_FORMATS = [(value.name, value.name) for value in WorkFormat.objects.all()]
COUNTRIES = [(value.name, value.name) for value in Country.objects.all()]


class AddVacancyForm(forms.Form):
    """Form for adding a new vacancy."""

    name = forms.CharField(label="Name", max_length=30, strip=True)
    company_name = forms.CharField(label="Company", max_length=30, strip=True)
    level = forms.ChoiceField(label="Level", choices=LEVELS)
    experience = forms.CharField(label="Experience", max_length=30, strip=True)
    min_salary = forms.IntegerField(label="Min Salary", min_value=0, required=False)
    max_salary = forms.IntegerField(label="Max Salary", min_value=0, required=False)
    description = forms.CharField(label='Description', widget=forms.Textarea, strip=True)
    employment_format = forms.MultipleChoiceField(
        label='Employment formats', widget=forms.CheckboxSelectMultiple, choices=EMPLOYMENT_FORMATS
    )
    work_format = forms.MultipleChoiceField(
        label='Work formats', widget=forms.CheckboxSelectMultiple, choices=WORK_FORMATS
    )
    country = forms.ChoiceField(label='Country', choices=COUNTRIES)
    city = forms.CharField(label='Available cities', widget=forms.Textarea, required=True)
    tags = forms.CharField(label="Tags", widget=forms.Textarea, validators=[ValidateMaxTagCount(max_count=5)])
    attachment = forms.FileField(
        label='Attachment',
        allow_empty_file=False,
        required=False,
        validators=[ValidateFileExtensions(['pdf']), ValidateFileSize(max_size=5_000_000)],
    )


class SearchVacancyForm(forms.Form):
    """Form for searching and filtering vacancies in the database."""

    template_name = "search_form_snippet.html"

    name = forms.CharField(label="Position", max_length=30, strip=True, required=False)
    company_name = forms.CharField(label="Company", max_length=30, strip=True, required=False)
    level = forms.ChoiceField(label="Level", choices=[("", "ALL")] + LEVELS, required=False)
    experience = forms.CharField(label="Experience", max_length=30, strip=True, required=False)
    min_salary = forms.IntegerField(label="Min Salary", min_value=0, required=False)
    max_salary = forms.IntegerField(label="Max Salary", min_value=0, required=False)
    tag = forms.CharField(label="Tags", required=False)
    employment_format = forms.MultipleChoiceField(
        label='Employment formats', widget=forms.CheckboxSelectMultiple, choices=EMPLOYMENT_FORMATS, required=False
    )
    work_format = forms.MultipleChoiceField(
        label='Work formats', widget=forms.CheckboxSelectMultiple, choices=WORK_FORMATS, required=False
    )
    country = forms.ChoiceField(label='Country', choices=[("", "ALL")] + COUNTRIES, required=False)
    city = forms.CharField(label='City', required=False)
