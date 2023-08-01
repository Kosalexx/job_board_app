"""
Services and business logic for working with data associated with registration and authentication.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

if TYPE_CHECKING:
    from core.business_logic.dto import RegistrationDTO
    from django.contrib.auth.models import User


logger = logging.getLogger(__name__)


def create_user(data: RegistrationDTO) -> None:
    """Records the added User data in the database."""
    logger.info('Get user creation request.', extra={"info": str(data)})

    user_model: User = get_user_model()
    created_user: User = user_model.objects.create_user(
        username=data.username, password=data.password, email=data.email, is_active=False
    )

    group = Group.objects.get(name=data.role)

    created_user.groups.add(group)
