"""
Services and business logic for working with data associated with registration and authentication.
"""

from __future__ import annotations

import logging
import time
import uuid
from typing import TYPE_CHECKING

from core.business_logic.exceptions import (
    ConfirmationCodeExpiredError,
    ConfirmationCodeNotExistError,
    UserAlreadyExistsError,
)
from core.models import EmailConfirmationCodes
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.db import IntegrityError
from django.urls import reverse

if TYPE_CHECKING:
    from core.business_logic.dto import RegistrationDTO
    from django.contrib.auth.models import AbstractBaseUser


logger = logging.getLogger(__name__)


def send_confirmation_email(user: AbstractBaseUser) -> None:
    """
    Send email to confirm a registration.
    Confirmation code is sent as a query parameter in a link.
    """

    confirmation_code = str(uuid.uuid4())
    expiration_time = settings.CONFIRMATION_CODE_LIVETIME + int(time.time())

    EmailConfirmationCodes.objects.create(code=confirmation_code, user=user, expiration=expiration_time)
    confirmation_url = settings.SERVER_HOST + reverse("confirm-signup") + f"?code={confirmation_code}"
    conf_message = (
        f'Please confirm email by clicking the link bellow. \n'
        f'------------------------------------------------\n'
        f' {confirmation_url} \n'
        f'------------------------------------------------\n'
        f'If you have received an email in error, please use the link bellow to deactivate the mailing:\n'
    )
    send_mail(
        subject="Confirm your email.",
        message=conf_message,
        from_email=settings.EMAIL_FROM,
        recipient_list=[user.email],
    )
    logger.info(msg="Confirmation link has been sent.", extra={"user": user.email, "code": confirmation_code})


def create_user(data: RegistrationDTO) -> None:
    """Records the added User data in the database."""
    logger.info('Get user creation request.', extra={"info": str(data)})

    user_model: AbstractBaseUser = get_user_model()
    try:
        created_user: AbstractBaseUser = user_model.objects.create_user(
            username=data.username, password=data.password, email=data.email, is_active=False
        )
        group = Group.objects.get(name=data.role)
        created_user.groups.add(group)
        logger.info(msg="Created user.", extra={"user_email": data.email})
    except IntegrityError as exc:
        logger.info(
            msg="Such email or username already exist.",
            extra={"user_email": data.email, "username": data.username},
        )
        raise UserAlreadyExistsError from exc
    send_confirmation_email(user=created_user)


def confirm_user_registration(confirmation_code: str) -> None:
    """
    Confirms user registration.

    Check the received confirmation code in query parameters with confirmation code in the database.
    Check the expiration time of the confirmation code. If the expiration time is expired, a new email
    with a new confirmation code will send.
    """
    try:
        code_data = EmailConfirmationCodes.objects.get(code=confirmation_code)
    except EmailConfirmationCodes.DoesNotExist as err:
        logger.error("Provided code doesn't exist.", exc_info=err, extra={'code': confirmation_code})
        raise ConfirmationCodeNotExistError from err

    if time.time() > code_data.expiration:
        logger.info(
            'The confirmation code has been removed because expiration time is up.',
            extra={"current_time": str(time.time()), "code_expiration": str(code_data.expiration)},
        )
        send_confirmation_email(user=code_data.user)
        logger.info(
            msg="The new confirmation code has been sent",
            extra={"new_code": EmailConfirmationCodes.objects.get(user=code_data.user), "user": code_data.user},
        )
        raise ConfirmationCodeExpiredError

    user = code_data.user
    user.is_active = True
    user.save()

    code_data.delete()
