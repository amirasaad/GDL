from io import BytesIO

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
        pdf = BytesIO(
            b"%PDF-1.0\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1"
            b">>endobj 3 0 obj<</Type/Page/MediaBox[0 0 3 3]>>endobj\nxref\n0 4\n0000000000 65535 f\n000000"
            b"0010 00000 n\n0000000053 00000 n\n0000000102 00000 n\ntrailer<</Size 4/Root 1 0 R>>\nstartxre"
            b"f\n149\n%EOF\n"
        )
        simple_file = SimpleUploadedFile(
            "txt.pdf", pdf.read(), content_type="application/pdf"
        )
        data = {"file": simple_file}
        resp = self.client.post(self.url, data)
        print(resp.data)
        assert resp.status_code == status.HTTP_201_CREATED

    def test_user_can_upload_file_wrong_ext_right_content_type(self):
        simple_file = SimpleUploadedFile(
            "txt.txt", b"some content", content_type="application/pdf"
        )
        data = {"file": simple_file}
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        self.assertIn("File extension “txt” is not allowed.", str(resp.data["file"]))

    def test_user_can_upload_document_not_pdf_or_pptx(self):
        simple_file = SimpleUploadedFile("txt.txt", b"some content")

        data = {"name": "test", "file": simple_file}
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        self.assertIn("File extension “txt” is not allowed.", str(resp.data["file"]))

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
