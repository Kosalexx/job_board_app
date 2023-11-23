from core.tests.utils import get_test_image
from django.core.files.uploadedfile import InMemoryUploadedFile


class QRApiAdapterMock:
    def get_qr(self, data: str) -> InMemoryUploadedFile:
        return get_test_image()
