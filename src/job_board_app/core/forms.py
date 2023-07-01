"""
"Core" app forms of job_board_app project.
"""

from django import forms

LEVELS = (("Intern", "Intern"), ("Junior", "Junior"), ("Middle", "Middle"), ("Senior", "Senior"))


class AddCompanyForm(forms.Form):
    """Form for adding a new company."""

    name = forms.CharField(label="Company name", max_length="30", strip=True)
    employees_number = forms.IntegerField(label="Employees number", min_value=1)


class AddVacancyForm(forms.Form):
    """Form for adding a new vacancy."""

    name = forms.CharField(label='Name', max_length="30", strip=True)
    company_name = forms.CharField(label="Company name", max_length="30", strip=True)
    level = forms.ChoiceField(label="Level", choices=LEVELS)
    experience = forms.CharField(label="Experience", max_length=30, strip=True)
    min_salary = forms.IntegerField(label="Min Salary", min_value=0, required=False)
    max_salary = forms.IntegerField(label="Max Salary", min_value=0, required=False)


class AddReviewForm(forms.Form):
    """Form for adding a new review."""

    user_name = forms.CharField(label='User name', max_length='30', strip=True)
    review_text = forms.CharField(label="Review text", max_length="800", strip=True)
