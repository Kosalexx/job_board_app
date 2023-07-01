"""
Configuration for the FORM_RENDERER setting in .settings.py.
"""

from django.forms.renderers import TemplatesSetting


class CustomFormRenderer(TemplatesSetting):
    """Configuration for the FORM_RENDERER setting."""

    form_template_name = "form_snippet.html"
