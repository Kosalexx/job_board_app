"""
Data transfer objects related to the AddCompanyForm, CompanyProfileFrom, and AddAddressForm forms.

DTOs are designed to move data between processes to reduce the number of method calls.
AddCompanyForm, CompanyProfileFrom, and AddAddressForm forms are described in the
core.presentation.forms.company module.
"""

from dataclasses import dataclass

from django.core.files.uploadedfile import InMemoryUploadedFile


@dataclass
class AddCompanyDTO:
    """DTO for storing and transferring data from AddCompanyForm."""

    name: str
    staff: int
    business_area: str


@dataclass
class AddCompanyProfileDTO:
    """DTO for storing and transferring data from AddCompanyProfileForm."""

    logo: InMemoryUploadedFile | None
    email: str
    founding_year: int
    description: str
    phone: str
    website_link: str
    linkedin_link: str | None
    github_link: str | None
    twitter_link: str | None


@dataclass
class AddAddressDTO:
    """DTO for storing and transferring data from AddAddressForm."""

    country: str
    city: str
    street_name: str
    home_number: int
    office_number: int | None
