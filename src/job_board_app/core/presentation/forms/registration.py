"""
"Core" app Registration forms of job_board_app project.
"""

from typing import Any

from django import forms


class RegistrationForm(forms.Form):
    """Form user registration."""

    username = forms.CharField(
        label='Username', max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={"class": "form-control"}), max_length=100
    )
    email = forms.EmailField(label='Enter Email', widget=forms.TextInput(attrs={"class": "form-control"}))
    role = forms.ChoiceField(label='Choose account type', widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, roles: list[tuple[str, str]], *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["role"].choices = roles
