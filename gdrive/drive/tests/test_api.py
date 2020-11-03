from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from gdrive.drive.models import GFile


class TestUploadFile(APITestCase):
    def setUp(self) -> None:
        self.url = "/api/files/"

    def test_user_retrieve_all_files(self):
        resp = self.client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

    def test_user_can_upload_file(self):
        simple_file = SimpleUploadedFile(
            "txt.pdf", b"some content", content_type="application/pdf"
        )
        data = {"file": simple_file}
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED

    def test_user_can_upload_file_wrong_ext_right_content_type(self):
        simple_file = SimpleUploadedFile(
            "txt.text", b"some content", content_type="application/pdf"
        )
        data = {"file": simple_file}
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED

    def test_user_can_upload_document_not_pdf_or_pptx(self):
        simple_file = SimpleUploadedFile("txt.txt", b"some content")

        data = {"name": "test", "file": simple_file}
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_name_from_file_path(self):
        file_name = "txt.pdf"
        doc = GFile.objects.create(
            file=SimpleUploadedFile(
                file_name, b"some content", content_type="application/pdf"
            )
        )
        resp = self.client.get(f"{self.url}{doc.id}/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["name"] == file_name
