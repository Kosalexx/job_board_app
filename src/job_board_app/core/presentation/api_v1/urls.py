from core.presentation.api_v1.views import (
    companies_api_controller,
    company_api_controller,
    vacancies_api_controller,
    vacancy_api_controller,
)
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Jobbard API",
        default_version="v1",
        description="REST API for job_board project",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('vacancies/', vacancies_api_controller, name='get-vacancies-api'),
    path('companies/', companies_api_controller, name='get-companies-api'),
    path('vacancies/<int:vacancy_id>/', vacancy_api_controller, name='get-vacancy-api'),
    path('companies/<int:company_id>/', company_api_controller, name='get-company-api'),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
