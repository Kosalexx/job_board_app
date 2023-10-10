"""
"Core" app Log-in forms of job_board_app project.
"""

from django import forms


class LoginForm(forms.Form):
    """Form user logging in."""

    username = forms.CharField(
        label='Username', max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={"class": "form-control"}), max_length=100
    )
