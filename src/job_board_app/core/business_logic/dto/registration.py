"""
Data transfer objects related to the RegistrationForm form.

DTOs are designed to move data between processes to reduce the number of method calls.
RegistrationForm form is described in the core.presentation.forms.registration module.
"""

from dataclasses import dataclass


@dataclass
class RegistrationDTO:
    """DTO for storing and transferring data from RegistrationForm."""

    username: str
    password: str
    email: str
    role: str

    def __str__(self) -> str:
        return f"username={self.username}, email={self.email}, role={self.role}"
