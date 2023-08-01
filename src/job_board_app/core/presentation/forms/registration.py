"""
"Core" app Registration forms of job_board_app project.
"""

from django import forms
from django.contrib.auth.models import Group

USER_TYPE_CHOICES = [(group.name, group.name) for group in Group.objects.all()]


class RegistrationForm(forms.Form):
    """Form user registration."""

    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=100)
    email = forms.EmailField(label='Enter Email')
    role = forms.ChoiceField(label='Choose account type', choices=USER_TYPE_CHOICES)
