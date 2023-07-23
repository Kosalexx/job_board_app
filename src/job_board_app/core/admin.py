"""
Admin config for "core" app job_board_app project.
"""

from core.models import Company, Level, Tag, Vacancy
from django.contrib import admin

# Register your models here.
admin.site.register(Company)
admin.site.register(Vacancy)
admin.site.register(Tag)
admin.site.register(Level)
