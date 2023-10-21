from core.presentation.api_v1.views import (
    companies_api_controller,
    company_api_controller,
    vacancies_api_controller,
    vacancy_api_controller,
)
from django.urls import path

urlpatterns = [
    path('vacancies/', vacancies_api_controller, name='get-vacancies-api'),
    path('companies/', companies_api_controller, name='get-companies-api'),
    path('vacancies/<int:vacancy_id>/', vacancy_api_controller, name='get-vacancy-api'),
    path('companies/<int:company_id>/', company_api_controller, name='get-company-api'),
]
