"""
Functions that transform data for further use by other parts of the app.
"""

from __future__ import annotations

import logging
from io import BytesIO
from sys import getsizeof
from uuid import uuid4

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

logger = logging.getLogger(__name__)


def replace_file_name_to_uuid(file: InMemoryUploadedFile) -> InMemoryUploadedFile:
    """Replaces the user's filename with the uuid4 standard name."""

    old_name = file.name
    file_extension = old_name.split('.')[-1]
    file_name = str(uuid4())
    file.name = file_name + '.' + file_extension
    logger.info(
        'Successfully replaced file name with the uuid4 standard name',
        extra={'old_file_name': old_name, 'new_file_name': file.name},
    )
    return file


def change_file_size(file: InMemoryUploadedFile) -> InMemoryUploadedFile:
    """Changes the size of uploaded images."""

    content_type = file.content_type
    if content_type is not None:
        file_format = content_type.split('/')[-1].upper()
    else:
        file_format = ''
    output = BytesIO()
    with Image.open(file) as image:
        image.thumbnail(size=(200, 150))
        image.save(output, format=file_format, quality=100)
    old_size = file.size
    new_size = getsizeof(output)
    file = InMemoryUploadedFile(
        file=output,
        field_name=file.field_name,
        name=file.name,
        content_type=file.content_type,
        size=getsizeof(output),
        charset=file.charset,
    )
    logger.info('Successfully changed file size', extra={"old_size": str(old_size), 'new_size': str(new_size)})
    return file
