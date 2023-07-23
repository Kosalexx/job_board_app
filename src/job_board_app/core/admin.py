"""
Admin config for "core" app job_board_app project.
"""

from django.contrib import admin

from .models import MyModel

# Register your models here.
admin.site.register(MyModel)
