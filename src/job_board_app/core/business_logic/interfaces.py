from typing import Protocol

from django.core.files.uploadedfile import InMemoryUploadedFile


class QRApiAdapterProtocol(Protocol):
    def get_qr(self, data: str) -> InMemoryUploadedFile:
        raise NotImplementedError
