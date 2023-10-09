"""
Data transfer objects related to the LoginForm form.

DTOs are designed to move data between processes to reduce the number of method calls.
RegistrationForm form is described in the core.presentation.forms.login module.
"""

from dataclasses import dataclass


@dataclass
class LoginDTO:
    """DTO for storing and transferring data from LoginForm."""

    username: str
    password: str

    def __str__(self) -> str:
        return f"username={self.username}"
