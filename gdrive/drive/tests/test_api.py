from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase


class TestUploadFile(APITestCase):
    def setUp(self) -> None:
        self.url = "/api/files/"

    def test_user_retrive_all_files(self):
        resp = self.client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

    def test_user_can_upload_document(self):
        simple_file = SimpleUploadedFile("txt.pdf", b"some content")

        data = {"name": "test", "file": simple_file}
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED

    def test_user_can_upload_document_not_pdf_or_pptx(self):
        simple_file = SimpleUploadedFile("txt.txt", b"some content")

        data = {"name": "test", "file": simple_file}
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
