"""
Functions that transform data for further use by other parts of the app.
"""

from __future__ import annotations

from io import BytesIO
from sys import getsizeof
from uuid import uuid4

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


def replace_file_name_to_uuid(file: InMemoryUploadedFile) -> InMemoryUploadedFile:
    """Replaces the user's filename with the uuid4 standard name."""

    file_extension = file.name.split('.')[-1]
    file_name = str(uuid4())
    file.name = file_name + '.' + file_extension
    return file


def change_file_size(file: InMemoryUploadedFile) -> InMemoryUploadedFile:
    """Changes the size of uploaded images."""

    file_format = file.content_type.split('/')[-1].upper()
    output = BytesIO()
    with Image.open(file) as image:
        image.thumbnail(size=(200, 150))
        image.save(output, format=file_format, quality=100)
    file = InMemoryUploadedFile(
        file=output,
        field_name=file.field_name,
        name=file.name,
        content_type=file.content_type,
        size=getsizeof(output),
        charset=file.charset,
    )
    return file
