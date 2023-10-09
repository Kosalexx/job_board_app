"""
Services and business logic for working authentication.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.business_logic.exceptions import InvalidAuthCredentialsError
from django.contrib.auth import authenticate

if TYPE_CHECKING:
    from core.business_logic.dto import LoginDTO
    from django.contrib.auth.models import AbstractBaseUser


logger = logging.getLogger(__name__)


def authenticate_user(data: LoginDTO) -> AbstractBaseUser:
    """Authentication of user."""
    user = authenticate(username=data.username, password=data.password)
    if user is not None:
        return user
    logger.error(msg="Invalid an email or a password.", extra={"user": data.username, "password": data.password})
    raise InvalidAuthCredentialsError
