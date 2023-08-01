"""
Admin config for "core" app job_board_app project.
"""

from core.models import (
    Address,
    BusinessArea,
    City,
    Company,
    CompanyProfile,
    Country,
    Employee,
    EmploymentFormat,
    Language,
    LanguageLevel,
    Level,
    Position,
    Response,
    ResponseStatus,
    Review,
    Tag,
    User,
    UsersLanguages,
    UsersProfile,
    Vacancy,
    WorkFormat,
    WorkStatus,
)
from django.contrib import admin

# Register your models here.
admin.site.register(Address)
admin.site.register(BusinessArea)
admin.site.register(City)
admin.site.register(CompanyProfile)
admin.site.register(Company)
admin.site.register(Country)
admin.site.register(Employee)
admin.site.register(EmploymentFormat)
admin.site.register(Language)
admin.site.register(LanguageLevel)
admin.site.register(Level)
admin.site.register(Position)
admin.site.register(Response)
admin.site.register(ResponseStatus)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(UsersProfile)
admin.site.register(User)
admin.site.register(UsersLanguages)
admin.site.register(WorkFormat)
admin.site.register(WorkStatus)
admin.site.register(Vacancy)
