from core.presentation.api_v1.views import get_companies_api_controller, get_vacancies_api_controller
from django.urls import path

urlpatterns = [
    path('vacancy/', get_vacancies_api_controller, name='get-vacancies-api'),
    path('company/', get_companies_api_controller, name='get-companies-api'),
]
