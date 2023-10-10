"""
"Core" app Vacancy forms of job_board_app project.
"""
from typing import Any

from core.presentation.common.validators import ValidateFileExtensions, ValidateFileSize, ValidateMaxTagCount
from django import forms


class AddVacancyForm(forms.Form):
    """Form for adding a new vacancy."""

    name = forms.CharField(label="Name", max_length=30, strip=True)
    company_name = forms.CharField(label="Company", max_length=30, strip=True)
    level = forms.ChoiceField(label="Level")
    experience = forms.CharField(label="Experience", max_length=30, strip=True)
    min_salary = forms.IntegerField(label="Min Salary", min_value=0, required=False)
    max_salary = forms.IntegerField(label="Max Salary", min_value=0, required=False)
    description = forms.CharField(label='Description', widget=forms.Textarea, strip=True)
    employment_format = forms.MultipleChoiceField(label='Employment formats', widget=forms.CheckboxSelectMultiple)
    work_format = forms.MultipleChoiceField(label='Work formats', widget=forms.CheckboxSelectMultiple)
    country = forms.ChoiceField(label='Country')
    city = forms.CharField(label='Available cities', widget=forms.Textarea, required=True)
    tags = forms.CharField(label="Tags", widget=forms.Textarea, validators=[ValidateMaxTagCount(max_count=5)])
    attachment = forms.FileField(
        label='Attachment',
        allow_empty_file=False,
        required=False,
        validators=[ValidateFileExtensions(['pdf']), ValidateFileSize(max_size=5_000_000)],
    )

    def __init__(
        self,
        levels: list[tuple[str, str]],
        employment_formats: list[tuple[str, str]],
        work_formats: list[tuple[str, str]],
        countries: list[tuple[str, str]],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.fields["level"].choices = levels
        self.fields["employment_format"].choices = employment_formats
        self.fields["work_format"].choices = work_formats
        self.fields["country"].choices = countries


class SearchVacancyForm(forms.Form):
    """Form for searching and filtering vacancies in the database."""

    template_name = "search_form_snippet.html"

    name = forms.CharField(label="Position", max_length=30, strip=True, required=False)
    company_name = forms.CharField(label="Company", max_length=30, strip=True, required=False)
    level = forms.ChoiceField(label="Level", choices=[("", "ALL")], required=False)
    experience = forms.CharField(label="Experience", max_length=30, strip=True, required=False)
    min_salary = forms.IntegerField(label="Min Salary", min_value=0, required=False)
    max_salary = forms.IntegerField(label="Max Salary", min_value=0, required=False)
    tag = forms.CharField(label="Tags", required=False)
    employment_format = forms.MultipleChoiceField(
        label='Employment formats', widget=forms.CheckboxSelectMultiple, required=False
    )
    work_format = forms.MultipleChoiceField(label='Work formats', widget=forms.CheckboxSelectMultiple, required=False)
    country = forms.ChoiceField(label='Country', required=False)
    city = forms.CharField(label='City', required=False)

    def __init__(
        self,
        levels: list[tuple[str, str]],
        employment_formats: list[tuple[str, str]],
        work_formats: list[tuple[str, str]],
        countries: list[tuple[str, str]],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.fields["level"].choices = levels
        self.fields["employment_format"].choices = employment_formats
        self.fields["work_format"].choices = work_formats
        self.fields["country"].choices = countries
