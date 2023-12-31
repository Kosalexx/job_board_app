"""
URL configuration for "core" app job_board_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from core.presentation.web.views import (
    add_company_controller,
    add_vacancy_controller,
    apply_vacancy_controller,
    companies_list_controller,
    get_company_controller,
    get_vacancy_controller,
    index_controller,
    login_controller,
    logout_controller,
    registration_confirmation,
    registration_controller,
    successfully_apply_controller,
)
from django.urls import path

urlpatterns = [
    path("", index_controller, name='index'),
    path("company/add/", add_company_controller, name="add-company"),
    path("company/", companies_list_controller, name="company-list"),
    path("vacancy/add/", add_vacancy_controller, name="add-vacancy"),
    path("vacancy/<int:vacancy_id>/", get_vacancy_controller, name="vacancy"),
    path("company/<int:company_id>/", get_company_controller, name="company"),
    path("signup/", registration_controller, name='signup'),
    path("confirmation/", registration_confirmation, name='confirm-signup'),
    path("signin/", login_controller, name='login'),
    path("logout/", logout_controller, name='logout'),
    path("vacancy/<int:vacancy_id>/apply/", apply_vacancy_controller, name='apply-vacancy'),
    path("vacancy/apply/success", successfully_apply_controller, name='post-apply'),
]
